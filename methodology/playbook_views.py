"""
Playbook views (GUI prototype - no backend logic).

These are stub views that render templates with mock data for UI prototyping.
Based on feature file: docs/features/playbooks.feature
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Mock data matching the Background section of playbooks.feature
MOCK_PLAYBOOKS = [
    {
        'id': 'AGILE-01',
        'name': 'Agile Development',
        'description': 'Iterative and incremental approach to software development emphasizing flexibility and customer collaboration.',
        'family': 'Development',
        'version': '2.1',
        'type': 'Methodology',
        'status': 'Active',
        'author': 'Ken Schwaber & Jeff Sutherland',
        'created_at': '2024-01-15',
        'updated_at': '2024-11-10',
    },
    {
        'id': 'SCRUM-01',
        'name': 'Scrum Framework',
        'description': 'Lightweight framework that helps people, teams and organizations generate value through adaptive solutions.',
        'family': 'Development',
        'version': '3.0',
        'type': 'Framework',
        'status': 'Active',
        'author': 'Scrum Alliance',
        'created_at': '2024-02-20',
        'updated_at': '2024-10-25',
    },
    {
        'id': 'TDD-01',
        'name': 'Test-Driven Development',
        'description': 'Software development approach where tests are written before the code that needs to pass those tests.',
        'family': 'Testing',
        'version': '1.5',
        'type': 'Practice',
        'status': 'Active',
        'author': 'Kent Beck',
        'created_at': '2024-03-10',
        'updated_at': '2024-11-01',
    },
    {
        'id': 'DEVOPS-01',
        'name': 'DevOps Practices',
        'description': 'Set of practices combining software development and IT operations to shorten development lifecycle.',
        'family': 'Operations',
        'version': '2.0',
        'type': 'Practice',
        'status': 'Active',
        'author': 'DevOps Institute',
        'created_at': '2024-04-05',
        'updated_at': '2024-10-15',
    },
    {
        'id': 'DDD-01',
        'name': 'Domain-Driven Design',
        'description': 'Approach to software development that centers on programming aligned with the domain model.',
        'family': 'Architecture',
        'version': '1.8',
        'type': 'Methodology',
        'status': 'Active',
        'author': 'Eric Evans',
        'created_at': '2024-05-12',
        'updated_at': '2024-09-30',
    },
    {
        'id': 'LEAN-01',
        'name': 'Lean Software Development',
        'description': 'Translation of lean manufacturing principles to software development with focus on eliminating waste.',
        'family': 'Development',
        'version': '1.2',
        'type': 'Methodology',
        'status': 'Draft',
        'author': 'Mary & Tom Poppendieck',
        'created_at': '2024-06-18',
        'updated_at': '2024-11-05',
    },
]


@login_required
def playbook_list(request):
    """
    Display list of playbooks as cards with filters and search.
    
    Implements: PB-1.1, PB-1.2, PB-1.3, PB-1.4
    GET /playbooks/
    """
    # Extract unique families for filter dropdown
    families = sorted(list(set(p['family'] for p in MOCK_PLAYBOOKS)))
    
    context = {
        'playbooks': MOCK_PLAYBOOKS,
        'families': families,
        'page_title': 'Playbooks',
    }
    return render(request, 'playbooks/list.html', context)


@login_required
def playbook_detail(request, playbook_id):
    """
    Display single playbook detail view.
    
    Implements: PB-2.1, PB-2.2
    GET /playbooks/<id>/
    """
    # Find playbook by ID
    playbook = next((p for p in MOCK_PLAYBOOKS if p['id'] == playbook_id), None)
    
    if not playbook:
        context = {
            'playbook_id': playbook_id,
            'page_title': 'Playbook Not Found',
        }
        return render(request, 'playbooks/404.html', context, status=404)
    
    context = {
        'playbook': playbook,
        'page_title': playbook['name'],
    }
    return render(request, 'playbooks/detail.html', context)


@login_required
def playbook_add(request):
    """
    Display form to create a new playbook.
    
    Implements: PB-3.1, PB-3.2, PB-3.3, PB-3.4, PB-3.5
    GET /playbooks/add/
    """
    context = {
        'mode': 'add',
        'page_title': 'Add Playbook',
        'playbook': None,
        'families': ['Development', 'Testing', 'Operations', 'Architecture', 'Design'],
        'types': ['Methodology', 'Framework', 'Practice'],
        'statuses': ['Draft', 'Active', 'Archived', 'Deprecated'],
    }
    return render(request, 'playbooks/form.html', context)


@login_required
def playbook_edit(request, playbook_id):
    """
    Display form to edit an existing playbook.
    
    Implements: PB-4.1, PB-4.2, PB-4.3
    GET /playbooks/<id>/edit/
    """
    # Find playbook by ID
    playbook = next((p for p in MOCK_PLAYBOOKS if p['id'] == playbook_id), None)
    
    if not playbook:
        context = {
            'playbook_id': playbook_id,
            'page_title': 'Playbook Not Found',
        }
        return render(request, 'playbooks/404.html', context, status=404)
    
    context = {
        'mode': 'edit',
        'page_title': f'Edit Playbook: {playbook["name"]}',
        'playbook': playbook,
        'families': ['Development', 'Testing', 'Operations', 'Architecture', 'Design'],
        'types': ['Methodology', 'Framework', 'Practice'],
        'statuses': ['Draft', 'Active', 'Archived', 'Deprecated'],
    }
    return render(request, 'playbooks/form.html', context)
