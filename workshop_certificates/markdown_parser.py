import os
import re

CHECKPOINT_PATTERN = re.compile(r'<!--\s*CHECKPOINT:\s*(?P<section>[^,]+),\s*(?P<name>[^,]+),\s*points=(?P<points>\d+)\s*-->')


def parse_checkpoints_from_markdown(md_dir):
    scenarios = []
    for root, _, files in os.walk(md_dir):
        for fname in files:
            if fname.endswith('.md'):
                path = os.path.join(root, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = CHECKPOINT_PATTERN.search(line)
                        if match:
                            scenarios.append({
                                'section': match.group('section').strip(),
                                'name': match.group('name').strip(),
                                'points': int(match.group('points')),
                                'file': path
                            })
    return scenarios

# Example usage:
# scenarios = parse_checkpoints_from_markdown('../docs')
# for s in scenarios:
#     print(s) 