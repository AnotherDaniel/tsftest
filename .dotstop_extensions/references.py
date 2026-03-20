import os
import requests
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from trudag.dotstop.core.reference.references import BaseReference, FileReference

class WebReference(BaseReference):
  def __init__(self, url: str) -> None:
        """
        References to arbitrary web pages.

        This reference fetches the page at the given URL using `requests` and exposes
        its content via the `content` property. The content is returned as UTF-8
        encoded bytes. Optional line anchors can be embedded in the URL (e.g.
        "https://example.com/file.txt#L10" or "https://example.com/file.txt#L5-L15")
        to highlight specific lines in the returned content with markdown blockquote
        prefix (> ).

        Args:
            url (str): URL of the webpage to reference. Must be a valid HTTP or HTTPS URL.
                       May optionally include line anchors like #L10 or #L10-L20.

        Notes:
            Network errors will raise `requests.RequestException` when accessing `content`.
            Line anchors are stripped before fetching but used to highlight lines in the result.
        """
        # allow optional line anchor embedded in the URL (e.g. "http://example.com/file#L12" or
        # "http://example.com/file#L5-L10"). record the bounds and strip the anchor before
        # passing to requests.get() so the URL is valid.
        start: int | None = None
        end: int | None = None
        if "#L" in url:
            base, anchor = url.split("#L", 1)
            if "-L" in anchor:
                a, b = anchor.split("-L", 1)
                try:
                    start = int(a)
                except ValueError:
                    start = None
                try:
                    end = int(b)
                except ValueError:
                    end = start
            else:
                try:
                    start = int(anchor)
                except ValueError:
                    start = None
            url = base
        self._url = url
        self._start = start
        self._end = end

  @classmethod
  def type(cls) -> str:
    return "webpage"

  @property
  def content(self) -> bytes:
    response = requests.get(self._url)
    raw = response.text.encode('utf-8')

    # if no anchor present just return raw bytes
    if self._start is None:
      return raw

    # highlight selected lines in markdown style by prefixing with '> '
    text = response.text
    lines = text.splitlines(keepends=True)
    start_val: int = self._start  # type: ignore[assignment]
    start_idx = max(start_val - 1, 0)
    end_val: int = self._end if self._end is not None else start_val  # type: ignore[assignment]
    end_idx = min(end_val, len(lines))
    out_lines: list[str] = []
    for idx, line in enumerate(lines, start=1):
      if start_idx <= idx - 1 < end_idx:
        out_lines.append(f"> {line}")
      else:
        out_lines.append(line)
    return "".join(out_lines).encode('utf-8')

  def as_markdown(self, filepath: None | str = None) -> str:
    return f"`{self._url}`"


class DownloadUrlReference(BaseReference):
  def __init__(self, url: str, description: str) -> None:
        """
        References a file download URL, e.g. pointing to a GitHub release artifact.

        This reference simply holds the download URL, and renders a useful markdown representation.

        Args:
            url (str): URL of the file to reference.
            decription (str): Brief description of the referenced file, for documentation/report generation purposes.

        Notes:
            -
        """
        self._url = url
        self._description = description

  @classmethod
  def type(cls) -> str:
    return "download_url"

  @property
  def content(self) -> bytes:
    try:
        response = requests.get(self._url)
        response.raise_for_status()
        return response.content
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Failed to connect to URL: {self._url}")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Request timed out for URL: {self._url}")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error for URL: {self._url}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Unexpected error downloading {self._url}: {e}") from e

  def as_markdown(self, filepath: None | str = None) -> str:
    return f"[{self._description}]({self._url})"

  def __str__(self) -> str:
        return f"{self._description} at {self._url}"


class OpenFastTraceReference(BaseReference):
  _index_cache: dict[str, dict[str, dict]] = {}

  def __init__(self, requirement_id: str) -> None:
        """
        References to an OpenFastTrace requirement idenfier.

        Parses an OFT aspec XML report (path taken from the OFT_ASPEC environment
        variable) and renders a concise summary for the given requirement.

        Args:
            requirement_id (str): OpenFastTrace requirement identifier.

        Notes:
            Requires the OFT_ASPEC environment variable to point at a valid
            aspec XML file.  The parsed index is cached at class level so that
            repeated calls (e.g. when the host tool processes many references)
            do not re-parse the XML each time.
        """
        self._requirement_id = str(requirement_id)

  @classmethod
  def type(cls) -> str:
    return "openfasttrace"

  @classmethod
  def _get_index(cls, aspec_path: str) -> dict[str, dict]:
    if aspec_path not in cls._index_cache:
        tree = ET.parse(aspec_path)  # noqa: S314 — trusted local file
        root = tree.getroot()
        index: dict[str, dict] = {}
        for specobjects in root.findall("specobjects"):
            doctype = specobjects.get("doctype", "")
            for so in specobjects.findall("specobject"):
                item_id = so.findtext("id", "")
                version = so.findtext("version", "")
                key = f"{doctype}~{item_id}~{version}"
                index[key] = {
                    "doctype": doctype,
                    "id": item_id,
                    "version": version,
                    "shortdesc": so.findtext("shortdesc", ""),
                    "status": so.findtext("status", ""),
                    "sourcefile": so.findtext("sourcefile", ""),
                    "sourceline": so.findtext("sourceline", ""),
                    "description": so.findtext("description", ""),
                    "element": so,
                }
        cls._index_cache[aspec_path] = index
    return cls._index_cache[aspec_path]

  @property
  def content(self) -> bytes:
    return self.as_markdown().encode("utf-8")

  @staticmethod
  def _spec_key(el: ET.Element) -> str:
    """Build a doctype~id~version key from an XML element."""
    return f"{el.findtext('doctype', '')}~{el.findtext('id', '')}~{el.findtext('version', '')}"

  @staticmethod
  def _source_link(sourcefile: str, sourceline: str) -> str:
    """Format a source file reference as a markdown link when possible."""
    label = f"{sourcefile}:{sourceline}" if sourceline else sourcefile
    server = os.environ.get("GITHUB_SERVER_URL", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    sha = os.environ.get("GITHUB_SHA", "")
    if server and repo and sha:
        url = f"{server}/{repo}/blob/{sha}/{urllib.parse.quote(sourcefile, safe='/')}"
        if sourceline:
            url += f"#L{sourceline}"
        return f"[{label}]({url})"
    return f"`{label}`"

  def _resolve_item(self, index: dict[str, dict]) -> dict | None:
    """Resolve requirement_id to an index entry, trying exact key, bare ID, and doctype~id."""
    spec_id = self._requirement_id
    item = index.get(spec_id)
    if item is not None:
        return item
    # Try matching by bare ID (without doctype~…~version prefix/suffix)
    matches = [v for v in index.values() if v["id"] == spec_id]
    if not matches:
        # Also try interpreting "doctype~id" format (no version)
        parts = spec_id.split("~", 1)
        if len(parts) == 2:
            dtype, bare_id = parts
            matches = [v for v in index.values()
                       if v["doctype"] == dtype and v["id"] == bare_id]
    if matches:
        # Prefer req-type items when multiple matches exist
        req_matches = [m for m in matches if m["doctype"] == "req"]
        return req_matches[0] if req_matches else matches[0]
    return None

  def as_markdown(self, filepath: None | str = None) -> str:
    aspec_path = os.environ.get("OFT_ASPEC", "")
    if not aspec_path:
        return "OFT_ASPEC is not set or empty; cannot extract OFT report information."

    index = self._get_index(aspec_path)
    item = self._resolve_item(index)
    if item is None:
        return f"Spec item '{self._requirement_id}' not found in OFT report ({aspec_path})"

    so: ET.Element = item["element"]
    coverage = so.find("coverage")

    # --- needs & coverage status ---
    needs: list[str] = []
    covered_types: set[str] = set()
    if coverage is not None:
        needs = [n.text or "" for n in coverage.findall("needscoverage/needsobj")]
        covered_types = {
            ct.text or "" for ct in coverage.findall("coveredTypes/coveredType")
        }

    shallow = (
        coverage.findtext("shallowCoverageStatus", "") if coverage is not None else ""
    )
    has_needs = len(needs) > 0
    is_ok = (shallow == "COVERED") if has_needs else True
    status_icon = "\u2713" if is_ok else "\u2717"

    needs_display = [n if n in covered_types else f"-{n}" for n in needs]

    # --- incoming links (items that cover this req) ---
    incoming: list[dict[str, str]] = []
    if coverage is not None:
        for cso in coverage.findall("coveringSpecObjects/coveringSpecObject"):
            c_key = self._spec_key(cso)
            src = index.get(c_key, {})
            incoming.append({
                "id": c_key,
                "sourcefile": src.get("sourcefile", ""),
                "sourceline": src.get("sourceline", ""),
            })

    # --- dependencies ---
    deps: list[str] = []
    deps_elem = so.find("dependencies")
    if deps_elem is not None:
        for d in deps_elem.findall("dependsOnSpecObject"):
            deps.append(self._spec_key(d))

    # --- assemble summary ---
    lines: list[str] = []
    full_id = f"{item['doctype']}~{item['id']}~{item['version']}"

    # Header with status, requirement name, and qualified ID
    lines.append(f"{status_icon} **{item['shortdesc']}** &mdash; `{full_id}`")

    # Requirement text
    if item["description"]:
        lines.append("")
        lines.append(f"> {item['description']}")

    lines.append("")

    # Compact metadata
    meta_parts = [f"**Source:** {self._source_link(item['sourcefile'], item['sourceline'])}"]
    if needs_display:
        meta_parts.append(f"**Needs:** {', '.join(needs_display)}")
    if shallow:
        meta_parts.append(f"**Coverage:** {shallow}")
    lines.append(" · ".join(meta_parts))

    # Covered by (items that implement/cover this req)
    if incoming:
        lines.append("")
        lines.append(f"**Covered by** ({len(incoming)}):")
        lines.append("")
        for inc in incoming:
            src = f" — {self._source_link(inc['sourcefile'], inc['sourceline'])}" if inc["sourcefile"] else ""
            lines.append(f"- `{inc['id']}`{src}")

    # Dependencies
    if deps:
        lines.append("")
        lines.append(f"**Depends on** ({len(deps)}):")
        lines.append("")
        for d in deps:
            lines.append(f"- `{d}`")

    return "\n".join(lines)

  def __str__(self) -> str:
    return f"OpenFastTrace requirement {self._requirement_id})"


class GithubFileReference(FileReference):
    DEFAULT_TOKEN_ENV_VAR = "GITHUB_TOKEN"

    def __init__(
        self,
        repository: str,
        path: str,
        public: bool = True,
        ref: str = "main",
        token: str = DEFAULT_TOKEN_ENV_VAR,
        **kwargs,
    ) -> None:
        """
        References to Artifacts that are regular files in a GitHub repository.

        For acessing non-public repositories, a valid [github token](https://docs.github.com/en/actions/concepts/security/github_token) 
        with sufficient read permissions must be available in the current environment.
        Several attempts are made to get a token, with the following precedence:

        1. User-specified `token` argument
        2. `$GITHUB_TOKEN`

        Args:
            repository (str): repository id
            path (str): Path to the Artifact, relative to the root of the repository
            public (bool): Indicate whether the repository is public (defaults to `true`, non-public repos require an access token to be set)
            ref (str, optional): Tag, branch or sha (defaults to `main`)
            token (str, optional): Environmental variable containing a suitable access token. Defaults to "GITHUB_TOKEN".
        """
        self._repository = repository
        # allow optional line anchor embedded in the path (e.g. "foo.txt#L12" or
        # "foo.txt#L5-L10"). record the bounds and strip the anchor before
        # converting to Path so the downloader still sees a valid filename.
        start: int | None = None
        end: int | None = None
        if "#L" in path:
            base, anchor = path.split("#L", 1)
            if "-L" in anchor:
                a, b = anchor.split("-L", 1)
                try:
                    start = int(a)
                except ValueError:
                    start = None
                try:
                    end = int(b)
                except ValueError:
                    end = start
            else:
                try:
                    start = int(anchor)
                except ValueError:
                    start = None
            path = base
        self._path = Path(path)
        self._start = start
        self._end = end
        self._public = public
        self._ref = ref
        self._token_env_var = token
        self._url = "https://github.com"

    @classmethod
    def type(cls) -> str:
        return "github"

    def _get_query(self) -> str:
        # https://github.com/<your_Github_username>/<your_repository_name>/blob/<branch_name>/<file_name>.<extension_name>
        query = f"{self._url}/{self._repository}/blob/{self._ref}/{urllib.parse.quote(str(self._path), safe='')}"
        if getattr(self, '_start', None) is not None:
            if self._end is None or self._end == self._start:
                query += f"#L{self._start}"
            else:
                query += f"#L{self._start}-L{self._end}"
        return query

    @property
    def content(self) -> bytes:
        query = self._get_query()
        try:
            req = urllib.request.Request(query)
        except Exception as exc:
            raise ReferenceError(f"Parse error for URL: {query}") from exc
        if not self._public:
            token = os.environ.get(self._token_env_var)
            if not token:
                token = os.environ.get(GithubFileReference.DEFAULT_TOKEN_ENV_VAR)
            if not token:
                err_msg = f"Access token must be set in ${self._token_env_var} or ${GithubFileReference.DEFAULT_TOKEN_ENV_VAR} for url {query}"
                raise ReferenceError(err_msg)
            req.add_header('Authorization', 'Bearer %s' % token)
        try:
            resp = urllib.request.urlopen(req)
        except Exception as exc:
            raise ReferenceError(f"Could not GET: {query}") from exc
        
        raw = resp.read()

        # if no anchor present just return raw bytes
        if getattr(self, '_start', None) is None:
            return raw

        start_val: int = self._start  # type: ignore[assignment]
        # highlight selected lines in markdown style by prefixing with '> '
        try:
            text = raw.decode('utf-8')
        except Exception:
            text = raw.decode('utf-8', errors='replace')
        lines = text.splitlines(keepends=True)
        start_idx = max(start_val - 1, 0)
        end_val: int = self._end if self._end is not None else start_val  # type: ignore[assignment]
        end_idx = min(end_val, len(lines))
        out_lines: list[str] = []
        for idx, line in enumerate(lines, start=1):
            if start_idx <= idx - 1 < end_idx:
                out_lines.append(f"> {line}")
            else:
                out_lines.append(line)
        return "".join(out_lines).encode('utf-8')

    @property
    def extension(self) -> str:
        return self._path.suffix

    def __str__(self) -> str:
        return self._get_query()
