#!/usr/bin/env python3
"""
Script: auto_archive.py
Mô tả: Tự động move files đã xử lý từ inputs/ sang archive/YYYY-MM/
       Claude gọi script này sau khi xử lý xong mỗi file
       
Usage:
  python scripts/auto_archive.py                    # Archive tất cả đã processed
  python scripts/auto_archive.py --file [filepath]  # Archive 1 file cụ thể
  python scripts/auto_archive.py --dry-run          # Preview không thực sự move
"""

import os, sys, shutil, json, argparse
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent
INPUTS    = WORKSPACE / "inputs"
ARCHIVE   = WORKSPACE / "archive"
DAILY_LOG = WORKSPACE / "daily_log"

PROCESSED_MARKER = "[PROCESSED]"
SUBFOLDERS = ["meetings", "notes", "pdfs", "emails", "reports", "decisions"]

def get_archive_dir() -> Path:
    """Tạo archive folder theo tháng hiện tại"""
    month_dir = ARCHIVE / datetime.now().strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    return month_dir

def is_processed(filepath: Path) -> bool:
    """Kiểm tra file đã được Claude xử lý chưa"""
    if filepath.suffix == ".md":
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            return PROCESSED_MARKER in content
        except:
            return False
    # PDF, docx — check xem có .processed marker file không
    marker = filepath.with_suffix(filepath.suffix + ".processed")
    return marker.exists()

def mark_as_processed(filepath: Path, summary: str = ""):
    """Thêm processed marker vào file .md"""
    if filepath.suffix == ".md":
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        marker = f"\n\n---\n{PROCESSED_MARKER}\n- **Processed at:** {timestamp}\n- **Summary:** {summary or 'Processed by Claude'}\n"
        filepath.write_text(content + marker, encoding="utf-8")
    else:
        # Tạo marker file riêng cho PDF/docx
        marker_file = filepath.with_suffix(filepath.suffix + ".processed")
        marker_file.write_text(
            f"Processed at: {datetime.now().isoformat()}\nSummary: {summary}",
            encoding="utf-8"
        )

def archive_file(filepath: Path, dry_run: bool = False) -> dict:
    """Move một file sang archive, trả về result dict"""
    archive_dir = get_archive_dir()
    subfolder   = filepath.parent.name
    dest_dir    = archive_dir / subfolder
    dest_dir.mkdir(exist_ok=True)

    dest = dest_dir / filepath.name
    # Tránh conflict tên file
    if dest.exists():
        stem = filepath.stem
        suffix = filepath.suffix
        dest = dest_dir / f"{stem}_{datetime.now().strftime('%H%M%S')}{suffix}"

    result = {
        "file":   str(filepath.relative_to(WORKSPACE)),
        "dest":   str(dest.relative_to(WORKSPACE)),
        "status": "dry-run" if dry_run else "archived"
    }

    if not dry_run:
        shutil.move(str(filepath), str(dest))
        # Move marker file nếu có (PDF/docx)
        marker = filepath.with_suffix(filepath.suffix + ".processed")
        if marker.exists():
            shutil.move(str(marker), str(dest_dir / marker.name))

    return result

def archive_all_processed(dry_run: bool = False) -> list:
    """Scan inputs/ và archive tất cả files đã processed"""
    results = []

    for subfolder in SUBFOLDERS:
        folder_path = INPUTS / subfolder
        if not folder_path.exists():
            continue

        for f in sorted(folder_path.iterdir()):
            if f.name.startswith("TEMPLATE_") or f.name.startswith("."):
                continue
            if f.suffix not in [".md", ".txt", ".pdf", ".docx", ".xlsx"]:
                continue
            if f.suffix == ".processed":
                continue

            if is_processed(f):
                result = archive_file(f, dry_run=dry_run)
                results.append(result)
                status = "→" if dry_run else "✅"
                print(f"  {status} {result['file']}")
                print(f"       → {result['dest']}")

    return results

def log_archive_run(results: list):
    """Ghi log archive run vào daily_log"""
    DAILY_LOG.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DAILY_LOG / f"{today}.md"

    log_entry = f"""
## 📦 Archive Run — {datetime.now().strftime('%H:%M')}
- Files archived: {len(results)}
"""
    for r in results:
        log_entry += f"  - `{r['file']}` → `{r['dest']}`\n"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

# ── MAIN ─────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Auto-archive processed input files")
    parser.add_argument("--file", help="Archive một file cụ thể theo path")
    parser.add_argument("--mark", help="Mark một file là đã processed")
    parser.add_argument("--summary", default="", help="Summary khi mark processed")
    parser.add_argument("--dry-run", action="store_true", help="Preview không move thực")
    args = parser.parse_args()

    print("=" * 55)
    print(f"AUTO ARCHIVE — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    if args.dry_run:
        print("MODE: DRY RUN (không move thực sự)")
    print("=" * 55)

    # Mark một file là processed
    if args.mark:
        filepath = WORKSPACE / args.mark
        if filepath.exists():
            mark_as_processed(filepath, args.summary)
            print(f"✅ Marked as processed: {args.mark}")
        else:
            print(f"❌ File not found: {args.mark}")
        return

    # Archive một file cụ thể
    if args.file:
        filepath = WORKSPACE / args.file
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            return
        result = archive_file(filepath, dry_run=args.dry_run)
        print(f"✅ Archived: {result['file']} → {result['dest']}")
        return

    # Archive tất cả processed files
    print("Scanning inputs/ for processed files...\n")
    results = archive_all_processed(dry_run=args.dry_run)

    print(f"\n{'='*55}")
    print(f"ARCHIVE SUMMARY")
    print(f"{'='*55}")
    if results:
        print(f"{'[DRY RUN] Would archive' if args.dry_run else 'Archived'}: {len(results)} files")
        if not args.dry_run:
            log_archive_run(results)
            print(f"Log: daily_log/{datetime.now().strftime('%Y-%m-%d')}.md")
    else:
        print("Không có file nào cần archive.")
        print("(Files cần có '[PROCESSED]' marker hoặc .processed file)")

    print("\nCác lệnh hữu ích:")
    print("  # Xem trước sẽ archive gì:")
    print("  python scripts/auto_archive.py --dry-run")
    print("  # Mark file là đã processed:")
    print("  python scripts/auto_archive.py --mark inputs/meetings/file.md --summary 'Action items đã tạo Jira'")
    print("=" * 55)

if __name__ == "__main__":
    main()
