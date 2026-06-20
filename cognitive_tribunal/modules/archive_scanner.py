"""
Module 1: Archive Scanner
Scans iCloud/Dropbox/drives with file classification and deduplication.
"""

import os
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime

from ..utils.file_utils import (
    FileClassifier, FileHasher, Deduplicator, extract_file_metadata
)


class ArchiveScanner:
    """
    Scans file archives and provides classification and deduplication.
    Supports local file systems, network drives, and common cloud storage mounts.
    """
    
    UNSAFE_PATHS_POSIX = {
        '/',
        '/bin',
        '/boot',
        '/dev',
        '/etc',
        '/lib',
        '/lib64',
        '/proc',
        '/root',
        '/sbin',
        '/sys',
        '/usr',
        '/var',
    }

    UNSAFE_PATHS_NT = {
        'C:\\Windows',
        'C:\\Program Files',
        'C:\\Program Files (x86)',
    }

    def __init__(self, exclude_patterns: Optional[List[str]] = None):
        """
        Initialize the archive scanner.
        
        Args:
            exclude_patterns: List of patterns to exclude (e.g., ['*.tmp', '__pycache__'])
        """
        self.exclude_patterns = exclude_patterns or [
            '__pycache__',
            '.git',
            '.svn',
            'node_modules',
            '.DS_Store',
            'Thumbs.db',
            '*.tmp',
            '*.swp',
        ]
        self.deduplicator = Deduplicator()
        self.scanned_files: List[Dict] = []
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'by_category': {},
            'errors': [],
        }
    
    def is_unsafe_path(self, path: Path) -> bool:
        """Check if path is considered unsafe to scan."""
        path_str = str(path)

        # Check Posix unsafe paths
        if path_str == '/':
            return True

        for unsafe in self.UNSAFE_PATHS_POSIX:
            if unsafe == '/':
                continue
            if path_str == unsafe or path_str.startswith(unsafe + os.sep):
                return True

        # Check Windows unsafe paths
        path_str_lower = path_str.lower().replace('/', '\\')
        for unsafe in self.UNSAFE_PATHS_NT:
            unsafe_lower = unsafe.lower()
            if path_str_lower == unsafe_lower or path_str_lower.startswith(unsafe_lower + '\\'):
                return True

        return False

    def should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded."""
        path_str = str(path)
        
        for pattern in self.exclude_patterns:
            # Simple pattern matching
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        
        return False
    
    def scan_directory(self, root_path: str, recursive: bool = True, max_depth: Optional[int] = None) -> Dict:
        """
        Scan a directory and classify all files.
        
        Args:
            root_path: Root directory to scan
            recursive: Whether to scan subdirectories
            max_depth: Maximum depth to scan (None for unlimited)
            
        Returns:
            Scan results dictionary
        """
        root = Path(root_path).resolve()
        
        if self.is_unsafe_path(root):
            return {'error': f"Security risk: Path is unsafe to scan: {root_path}"}

        if not root.exists():
            return {'error': f"Path does not exist: {root_path}"}
        
        if not root.is_dir():
            return {'error': f"Path is not a directory: {root_path}"}
        
        print(f"Scanning directory: {root}")
        self.scanned_files = []
        self.deduplicator = Deduplicator()
        self.stats = {
            'total_files': 0,
            'total_size': 0,
            'by_category': {},
            'errors': [],
        }
        
        self._scan_recursive(root, current_depth=0, max_depth=max_depth, recursive=recursive)
        
        return self.get_results()
    
    def _scan_recursive(self, path: Path, current_depth: int, max_depth: Optional[int], recursive: bool):
        """Recursively scan a directory."""
        if max_depth is not None and current_depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                if self.should_exclude(item):
                    continue
                
                if item.is_file():
                    self._process_file(item)
                elif item.is_dir() and recursive:
                    self._scan_recursive(item, current_depth + 1, max_depth, recursive)
        except PermissionError as e:
            self.stats['errors'].append(f"Permission denied: {path}")
        except Exception as e:
            self.stats['errors'].append(f"Error scanning {path}: {str(e)}")
    
    def _process_file(self, file_path: Path):
        """Process a single file."""
        try:
            metadata = extract_file_metadata(file_path)
            
            # Update statistics
            self.stats['total_files'] += 1
            self.stats['total_size'] += metadata.get('size', 0)
            
            category = metadata.get('category', 'other')
            self.stats['by_category'][category] = self.stats['by_category'].get(category, 0) + 1
            
            # Add to deduplicator
            self.deduplicator.add_file(file_path)
            
            # Store file info
            self.scanned_files.append(metadata)
            
        except Exception as e:
            self.stats['errors'].append(f"Error processing {file_path}: {str(e)}")
    
    def scan_multiple_locations(self, locations: List[str]) -> Dict:
        """
        Scan multiple archive locations.
        
        Args:
            locations: List of directory paths to scan
            
        Returns:
            Combined scan results
        """
        all_results = {
            'locations': {},
            'combined_stats': {
                'total_files': 0,
                'total_size': 0,
                'by_category': {},
                'errors': [],
            }
        }
        
        for location in locations:
            print(f"\nScanning location: {location}")
            results = self.scan_directory(location)
            all_results['locations'][location] = results
            
            # Aggregate statistics
            if 'stats' in results:
                stats = results['stats']
                all_results['combined_stats']['total_files'] += stats.get('total_files', 0)
                all_results['combined_stats']['total_size'] += stats.get('total_size', 0)
                
                for category, count in stats.get('by_category', {}).items():
                    all_results['combined_stats']['by_category'][category] = \
                        all_results['combined_stats']['by_category'].get(category, 0) + count
                
                all_results['combined_stats']['errors'].extend(stats.get('errors', []))
        
        return all_results
    
    def get_results(self) -> Dict:
        """Get comprehensive scan results."""
        duplicates = self.deduplicator.find_duplicates()
        dedup_stats = self.deduplicator.get_stats()
        
        # Calculate potential space savings
        space_wasted = 0
        for duplicate_group in duplicates.values():
            if duplicate_group:
                # All duplicates except one can be removed
                file_size = Path(duplicate_group[0]).stat().st_size if Path(duplicate_group[0]).exists() else 0
                space_wasted += file_size * (len(duplicate_group) - 1)
        
        return {
            'stats': self.stats,
            'files': self.scanned_files,
            'deduplication': {
                'stats': dedup_stats,
                'duplicates': {k: [str(p) for p in v] for k, v in duplicates.items()},
                'potential_space_savings': space_wasted,
            },
            'scan_timestamp': datetime.now().isoformat(),
        }
    
    def get_files_by_category(self, category: str) -> List[Dict]:
        """Get all files of a specific category."""
        return [f for f in self.scanned_files if f.get('category') == category]
    
    def get_large_files(self, min_size_mb: float = 10.0) -> List[Dict]:
        """Get files larger than specified size."""
        min_size_bytes = min_size_mb * 1024 * 1024
        return [f for f in self.scanned_files if f.get('size', 0) > min_size_bytes]
    
    def get_old_files(self, days_old: int = 365) -> List[Dict]:
        """Get files not modified in specified days."""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days_old)
        
        old_files = []
        for file_info in self.scanned_files:
            try:
                modified = datetime.fromisoformat(file_info.get('modified', ''))
                if modified < cutoff:
                    old_files.append(file_info)
            except:
                continue
        
        return old_files
