"""
Activity Graph Service for Graphviz visualization.

Generates SVG flow diagrams of activities within workflows using Graphviz.
Supports phase grouping, clickable nodes, and status-based styling.
"""

import logging
import graphviz
from django.urls import reverse
from methodology.models import Activity

logger = logging.getLogger(__name__)


class ActivityGraphService:
    """
    Service for generating Graphviz-based activity flow diagrams.
    
    Provides visual representation of activities with:
    - Sequential flow arrows
    - Phase grouping (if phases exist)
    - Clickable nodes linking to activity detail
    - Status-based node coloring
    - Dependency indicators
    """
    
    def generate_activities_graph(self, workflow, playbook):
        """
        Generate Graphviz flow diagram of activities in a workflow.
        
        Creates an SVG representation showing:
        - Activities as nodes with name and status
        - Sequential flow based on order field
        - Phase grouping using Graphviz subgraph clusters
        - Clickable nodes with href to activity detail
        - Status-based colors (green=completed, blue=in_progress, red=blocked, gray=not_started)
        
        :param workflow: Workflow instance containing activities
        :type workflow: methodology.models.Workflow
        :param playbook: Playbook instance (parent of workflow, used for URL generation)
        :type playbook: methodology.models.Playbook
        :return: SVG markup as string, or None if no activities exist
        :rtype: str or None
        :raises graphviz.backend.ExecutableNotFound: If Graphviz is not installed on system
        
        Example usage:
            >>> service = ActivityGraphService()
            >>> svg = service.generate_activities_graph(workflow, playbook)
            >>> # Returns: "<svg width='800' height='600'>...</svg>"
        
        Example with no activities:
            >>> svg = service.generate_activities_graph(empty_workflow, playbook)
            >>> # Returns: None
        """
        logger.info(f"Generating activity graph for workflow {workflow.pk}")
        
        # Fetch activities for workflow
        activities = Activity.objects.filter(workflow=workflow).order_by('order')
        
        if not activities.exists():
            logger.info(f"No activities found for workflow {workflow.pk}")
            return None
        
        try:
            # Create directed graph
            dot = graphviz.Digraph(comment=f'{workflow.name} Activities')
            dot.attr(rankdir='TB')  # Top to bottom layout
            dot.attr('node', shape='box', style='filled,rounded', fontname='Arial')
            dot.attr('edge', fontname='Arial')
            
            # Check if activities have phases
            has_phases = self._has_phases(activities)
            
            if has_phases:
                # Group activities by phase
                phase_groups = self._group_activities_by_phase(activities)
                
                # Create subgraph cluster for each phase
                for phase_name, phase_activities in phase_groups.items():
                    cluster_name = f'cluster_{phase_name.lower().replace(" ", "_")}'
                    with dot.subgraph(name=cluster_name) as subg:
                        subg.attr(label=phase_name, style='filled', color='lightgrey')
                        
                        # Add activity nodes within this phase
                        for activity in phase_activities:
                            self._add_activity_node(subg, activity, playbook, workflow)
            else:
                # No phases - add all activities directly
                for activity in activities:
                    self._add_activity_node(dot, activity, playbook, workflow)
            
            # Add edges between activities (sequential flow)
            activity_list = list(activities)
            for i in range(len(activity_list) - 1):
                current = activity_list[i]
                next_activity = activity_list[i + 1]
                dot.edge(f'activity_{current.pk}', f'activity_{next_activity.pk}')
            
            # Generate SVG
            svg_bytes = dot.pipe(format='svg')
            svg_str = svg_bytes.decode('utf-8')
            
            logger.info(f"Generated SVG graph for workflow {workflow.pk} with {activities.count()} activities")
            return svg_str
            
        except Exception as e:
            logger.error(f"Error generating activity graph for workflow {workflow.pk}: {str(e)}")
            raise
    
    def _get_activity_color(self, status):
        """
        Get Graphviz color for activity node based on status.
        
        Color mapping:
        - completed: lightgreen
        - in_progress: lightblue
        - blocked: lightcoral
        - not_started: lightgray
        
        :param status: Activity status from STATUS_CHOICES
        :type status: str
        :return: Graphviz color name
        :rtype: str
        
        Example:
            >>> service._get_activity_color('completed')
            'lightgreen'
        """
        color_map = {
            'completed': 'lightgreen',
            'in_progress': 'lightblue',
            'blocked': 'lightcoral',
            'not_started': 'lightgray',
        }
        return color_map.get(status, 'lightgray')
    
    def _create_activity_node_label(self, activity):
        """
        Create formatted label for activity node.
        
        Format: "{activity.name}\\n{status_display}"
        Uses newline escape for multi-line display in Graphviz.
        
        :param activity: Activity instance
        :type activity: methodology.models.Activity
        :return: Formatted label string with escaped newline
        :rtype: str
        
        Example:
            >>> label = service._create_activity_node_label(activity)
            >>> # Returns: "Design Component\\nIn Progress"
        """
        status_display = activity.get_status_display()
        label = f"{activity.name}\\n{status_display}"
        
        # Add dependency indicator if present
        if activity.has_dependencies:
            label += "\\n[Has Dependencies]"
        
        return label
    
    def _get_activity_detail_url(self, activity, playbook, workflow):
        """
        Generate URL to activity detail page.
        
        :param activity: Activity instance
        :type activity: methodology.models.Activity
        :param playbook: Playbook instance
        :type playbook: methodology.models.Playbook
        :param workflow: Workflow instance
        :type workflow: methodology.models.Workflow
        :return: Full URL path to activity detail
        :rtype: str
        
        Example:
            >>> url = service._get_activity_detail_url(activity, playbook, workflow)
            >>> # Returns: "/playbooks/1/workflows/2/activities/3/"
        """
        return reverse('activity_detail', kwargs={
            'playbook_pk': playbook.pk,
            'workflow_pk': workflow.pk,
            'activity_pk': activity.pk
        })
    
    def _has_phases(self, activities):
        """
        Check if any activity has a phase assigned.
        
        :param activities: QuerySet or list of Activity instances
        :type activities: django.db.models.QuerySet or list
        :return: True if at least one activity has phase field set
        :rtype: bool
        
        Example:
            >>> service._has_phases([activity1, activity2])
            True  # If any has phase != None
        """
        return any(activity.phase for activity in activities)
    
    def _group_activities_by_phase(self, activities):
        """
        Group activities by their phase field.
        
        Returns dict with phase names as keys and lists of activities as values.
        Activities without phase go into 'Unassigned' group.
        
        :param activities: QuerySet or list of Activity instances
        :type activities: django.db.models.QuerySet or list
        :return: Dict mapping phase names to activity lists
        :rtype: dict
        
        Example:
            >>> groups = service._group_activities_by_phase(activities)
            >>> # Returns: {'Planning': [act1, act2], 'Execution': [act3]}
        """
        phase_groups = {}
        for activity in activities:
            phase = activity.phase or 'Unassigned'
            if phase not in phase_groups:
                phase_groups[phase] = []
            phase_groups[phase].append(activity)
        return phase_groups
    
    def _add_activity_node(self, graph, activity, playbook, workflow):
        """
        Add activity node to Graphviz graph with styling and href.
        
        :param graph: Graphviz graph or subgraph instance
        :param activity: Activity instance to add
        :param playbook: Playbook instance for URL generation
        :param workflow: Workflow instance for URL generation
        """
        node_id = f'activity_{activity.pk}'
        label = self._create_activity_node_label(activity)
        color = self._get_activity_color(activity.status)
        url = self._get_activity_detail_url(activity, playbook, workflow)
        
        graph.node(
            node_id,
            label=label,
            fillcolor=color,
            href=url,
            target='_top'  # Opens in full page, not iframe
        )
