from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    ".gitignore",
    "prompts/01-prompt-nome-podcast.md",
    "prompts/01-1-prompt-correcao-nome-podcast.md",
    "prompts/02-prompt-roteiro-episodio-01.md",
    "prompts/02-1-prompt-ajuste-narracao-elevenlabs.md",
    "prompts/02-2-prompt-otimizacao-roteiro-elevenlabs.md",
    "prompts/02-3-prompt-reducao-roteiro-tempo-elevenlabs.md",
    "prompts/03-prompt-capa-podcast.md",
    "prompts/03-1-prompt-correcao-capa-paleta-fiap-sentrya.md",
    "script/episodio-01-roteiro-final.md",
    "docs/validacao-audio-elevenlabs.md",
    "docs/validacao-capa-podcast.md",
    "assets/capa-podcast-seguranca-em-agentes-de-ia.png",
    "output/episodio-01-seguranca-em-agentes-de-ia.mp3",
]

EXPECTED_DIRS = [
    "prompts",
    "script",
    "docs",
    "assets",
    "output",
    "scripts",
]

NO_GITKEEP_DIRS = [
    "prompts",
    "script",
    "docs",
    "assets",
    "output",
]

TEXT_EXTENSIONS = {
    ".md",
    ".py",
    ".txt",
    ".yml",
    ".yaml",
    ".gitignore",
}

SENSITIVE_WARN_PATTERNS = [
    "sk-",
    "ghp_",
    "github_pat_",
    "xoxb-",
    "AIza",
    "BEGIN PRIVATE KEY",
    "OPENAI_API_KEY=",
    "GEMINI_API_KEY=",
    "ELEVENLABS_API_KEY=",
]

SECRET_ASSIGNMENT_PREFIXES = [
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "ELEVENLABS_API_KEY",
]

PROHIBITED_DIR_NAMES = {
    "node_modules",
    "dist",
    "build",
}

PROHIBITED_FILE_NAMES = {
    ".env",
    ".DS_Store",
    "Thumbs.db",
}

PROHIBITED_SUFFIXES = (
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".log",
    ".zip",
    ".rar",
    ".7z",
    ".tmp",
    ".temp",
)


def relative(path):
    return path.relative_to(ROOT).as_posix()


def ok(message):
    print(f"[OK] {message}")


def warn(message):
    print(f"[WARN] {message}")


def error(errors, message):
    print(f"[ERROR] {message}")
    errors.append(message)


def iter_repository_paths():
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        yield path


def is_text_file(path):
    if path.name == ".gitignore":
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def has_real_secret_assignment(line):
    stripped = line.strip()
    if stripped.startswith("#") or stripped.startswith("-"):
        return False

    for prefix in SECRET_ASSIGNMENT_PREFIXES:
        marker = f"{prefix}="
        if marker not in stripped:
            continue

        value = stripped.split(marker, 1)[1].strip().strip("\"'")
        if value and value.lower() not in {"valor", "example", "exemplo", "your_key_here"}:
            return True

    return False


def validate_required_files(errors):
    # Validate required files / Valida arquivos obrigatórios
    missing = []
    for file_name in REQUIRED_FILES:
        path = ROOT / file_name
        if not path.is_file():
            missing.append(file_name)

    if missing:
        for file_name in missing:
            error(errors, f"Required file missing: {file_name}")
    else:
        ok("All required files exist.")


def validate_expected_dirs(errors):
    # Validate expected directories / Valida pastas esperadas
    missing = []
    for dir_name in EXPECTED_DIRS:
        path = ROOT / dir_name
        if not path.is_dir():
            missing.append(dir_name)

    if missing:
        for dir_name in missing:
            error(errors, f"Expected directory missing: {dir_name}/")
    else:
        ok("All expected directories exist.")


def validate_extensions(errors):
    # Validate file extensions / Valida extensões dos arquivos
    expected_extensions = {
        "assets/capa-podcast-seguranca-em-agentes-de-ia.png": ".png",
        "output/episodio-01-seguranca-em-agentes-de-ia.mp3": ".mp3",
    }

    for file_name in REQUIRED_FILES:
        if file_name.startswith(("prompts/", "script/", "docs/")):
            expected_extensions[file_name] = ".md"

    for file_name, expected_suffix in expected_extensions.items():
        path = ROOT / file_name
        if path.suffix.lower() != expected_suffix:
            error(errors, f"Invalid extension for {file_name}: expected {expected_suffix}")

    if not errors:
        ok("Required file extensions are valid.")
    else:
        ok("Extension validation completed.")


def validate_prohibited_files(errors):
    # Validate prohibited files and folders / Valida arquivos e pastas proibidos
    found = []

    for path in iter_repository_paths():
        name = path.name
        lower_name = name.lower()

        if path.is_dir() and name in PROHIBITED_DIR_NAMES:
            found.append(relative(path))
            continue

        if not path.is_file():
            continue

        if name in PROHIBITED_FILE_NAMES:
            found.append(relative(path))
        elif name.startswith(".env."):
            found.append(relative(path))
        elif lower_name.endswith(PROHIBITED_SUFFIXES):
            found.append(relative(path))
        elif name.endswith(("~", ".swp", ".swo")):
            found.append(relative(path))

    if found:
        for file_name in found:
            error(errors, f"Prohibited file or directory found: {file_name}")
    else:
        ok("No prohibited files or directories found.")


def validate_gitkeep(errors):
    # Validate obsolete .gitkeep files / Valida .gitkeep indevidos
    found = []
    for dir_name in NO_GITKEEP_DIRS:
        path = ROOT / dir_name / ".gitkeep"
        if path.exists():
            found.append(relative(path))

    if found:
        for file_name in found:
            error(errors, f"Unexpected .gitkeep found: {file_name}")
    else:
        ok("No obsolete .gitkeep files found.")


def validate_sensitive_content(errors):
    # Validate sensitive content patterns / Valida padrões de conteúdo sensível
    warnings = []
    current_script = Path(__file__).resolve()

    for path in iter_repository_paths():
        if not path.is_file() or not is_text_file(path):
            continue
        if path.resolve() == current_script:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warn(f"Could not read text file as UTF-8: {relative(path)}")
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if has_real_secret_assignment(line):
                error(errors, f"Possible real secret assignment in {relative(path)}:{line_number}")

            for pattern in SENSITIVE_WARN_PATTERNS:
                if pattern in line:
                    warnings.append(f"{relative(path)}:{line_number} contains pattern {pattern!r}")

    if warnings:
        for message in warnings:
            warn(message)
    else:
        ok("No sensitive content patterns found in text files.")


def validate_file_sizes(errors):
    # Validate minimum file sizes / Valida tamanhos mínimos dos arquivos
    checks = [
        ("output/episodio-01-seguranca-em-agentes-de-ia.mp3", 100 * 1024, "MP3 final"),
        ("assets/capa-podcast-seguranca-em-agentes-de-ia.png", 100 * 1024, "PNG final"),
        ("README.md", 500, "README"),
        ("script/episodio-01-roteiro-final.md", 1000, "Roteiro final"),
    ]

    for file_name, minimum_size, label in checks:
        path = ROOT / file_name
        if not path.is_file():
            error(errors, f"{label} does not exist: {file_name}")
            continue

        size = path.stat().st_size
        if size <= minimum_size:
            error(errors, f"{label} is too small: {file_name} has {size} bytes")
        else:
            ok(f"{label} size is valid: {file_name} has {size} bytes.")


def main():
    errors = []

    validate_required_files(errors)
    validate_expected_dirs(errors)
    validate_extensions(errors)
    validate_prohibited_files(errors)
    validate_gitkeep(errors)
    validate_sensitive_content(errors)
    validate_file_sizes(errors)

    if errors:
        print(f"[ERROR] Repository validation failed with {len(errors)} error(s).")
        return 1

    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
