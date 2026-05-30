#!/usr/bin/env python3
"""
Pipeline Automation MCP Server

Tools for executing and validating pipeline stages across
company and studio pipelines.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("Pipeline Automation")

# Workspace root from environment
WORKSPACE_ROOT = Path(os.getenv("WORKSPACE_ROOT", "."))


class PipelineManager:
    """Manage pipeline stage execution and validation"""
    
    COMPANY_STAGES = {
        0: "Problem Validation",
        1: "Requirements → PRD + SRD",
        2: "PRD → Web Prototype + IDS",
        3: "Prototype → UML Engineering Package",
        4: "UML → Implementation Plan + Gantt",
        5: "Plan → Software Development",
        6: "Development → Arch. & Conformance Review",
        7: "Arch. Review → Automated Testing",
        8: "Testing → Integrity Verification",
        9: "Integrity Verification → Translation Production",
        10: "Translation Production → Release Readiness Check",
        11: "Live Operations",
    }
    
    STUDIO_STAGES = {
        0: "Art Direction + Style Guide",
        1: "Concept (GDD + PRD + SRD)",
        2: "Prototype (Playable + GDS)",
        3: "Vertical Slice",
        4: "Production Planning",
        5: "Full Production",
        6: "Automated Testing",
        7: "Soft Launch Prep",
        8: "Soft Launch",
        9: "Global Launch Readiness",
        10: "Live Ops",
    }
    
    USER_APPROVAL_STAGES = {
        "company": [1, 2, 3, 4, 6, 7, 10],
        "studio": [1, 2, 3, 4, 6, 7, 8, 9],
    }
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
    
    def get_project_path(self, project_path: str) -> Path:
        """Get full project path"""
        return self.workspace_root / project_path
    
    def read_progress(self, project_path: str) -> Optional[Dict[str, Any]]:
        """Read progress.md file"""
        progress_file = self.get_project_path(project_path) / "progress.md"
        
        if not progress_file.exists():
            return None
        
        try:
            content = progress_file.read_text(encoding="utf-8")
            # Simple parsing - extract current stage
            lines = content.split("\n")
            current_stage = None
            
            for line in lines:
                if "Current Stage:" in line:
                    # Extract stage number
                    parts = line.split(":")
                    if len(parts) > 1:
                        stage_info = parts[1].strip()
                        if stage_info and stage_info[0].isdigit():
                            current_stage = int(stage_info[0])
            
            return {
                "current_stage": current_stage,
                "content": content,
            }
        except Exception as e:
            return {"error": str(e)}
    
    def validate_stage_gate(
        self, 
        stage: int, 
        project_path: str, 
        pipeline_type: str = "company"
    ) -> Dict[str, Any]:
        """Validate pipeline stage gate requirements"""
        
        stages = self.COMPANY_STAGES if pipeline_type == "company" else self.STUDIO_STAGES
        
        if stage not in stages:
            return {
                "passed": False,
                "error": f"Invalid stage: {stage}",
            }
        
        # Check if stage requires user approval
        requires_approval = stage in self.USER_APPROVAL_STAGES.get(pipeline_type, [])
        
        # Check for required deliverables
        project_dir = self.get_project_path(project_path)
        issues = []
        
        # Stage-specific validation
        if stage == 1:
            # Check for PRD and SRD
            if not (project_dir / "prd.md").exists():
                issues.append("Missing PRD (prd.md)")
            if not (project_dir / "srd.md").exists():
                issues.append("Missing SRD (srd.md)")
        
        elif stage == 3 and pipeline_type == "company":
            # Check for UML package
            if not (project_dir / "uml-package").exists():
                issues.append("Missing UML package directory")
            if not (project_dir / "adr").exists():
                issues.append("Missing ADR directory")
            if not (project_dir / "tsd.md").exists():
                issues.append("Missing TSD (tsd.md)")
        
        elif stage == 4:
            # Check for implementation plan
            if not (project_dir / "implementation-plan.md").exists():
                issues.append("Missing implementation plan")
            if not (project_dir / "gantt.md").exists():
                issues.append("Missing Gantt chart")
        
        return {
            "passed": len(issues) == 0,
            "stage": stage,
            "stage_name": stages[stage],
            "requires_user_approval": requires_approval,
            "issues": issues,
            "pipeline_type": pipeline_type,
        }
    
    def advance_stage(
        self, 
        stage: int, 
        project_path: str,
        pipeline_type: str = "company"
    ) -> Dict[str, Any]:
        """Advance project to next pipeline stage"""
        
        # Validate current stage first
        validation = self.validate_stage_gate(stage, project_path, pipeline_type)
        
        if not validation["passed"]:
            return {
                "success": False,
                "error": "Stage validation failed",
                "issues": validation["issues"],
            }
        
        # Update progress.md
        project_dir = self.get_project_path(project_path)
        progress_file = project_dir / "progress.md"
        
        new_stage = stage + 1
        stages = self.COMPANY_STAGES if pipeline_type == "company" else self.STUDIO_STAGES
        
        if new_stage not in stages:
            return {
                "success": False,
                "error": f"No stage {new_stage} in {pipeline_type} pipeline",
            }
        
        # Update progress file
        try:
            if progress_file.exists():
                content = progress_file.read_text(encoding="utf-8")
                # Update current stage line
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    if "Current Stage:" in line:
                        lines[i] = f"**Current Stage:** {new_stage} ({stages[new_stage]})"
                    elif f"Stage {stage}:" in line:
                        lines[i] = f"- [x] Stage {stage}: {stages[stage]}"
                
                progress_file.write_text("\n".join(lines), encoding="utf-8")
            
            return {
                "success": True,
                "old_stage": stage,
                "new_stage": new_stage,
                "new_stage_name": stages[new_stage],
                "message": f"Advanced to Stage {new_stage}: {stages[new_stage]}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update progress: {e}",
            }


# Initialize pipeline manager
pipeline_manager = PipelineManager(WORKSPACE_ROOT)


@mcp.tool()
def validate_stage_gate(
    stage: int, 
    project_path: str, 
    pipeline_type: str = "company"
) -> str:
    """
    Validate pipeline stage gate requirements.
    
    Args:
        stage: Stage number to validate
        project_path: Relative path to project from workspace root
        pipeline_type: "company" or "studio" (default: "company")
    
    Returns:
        JSON string with validation results
    """
    result = pipeline_manager.validate_stage_gate(stage, project_path, pipeline_type)
    return json.dumps(result, indent=2)


@mcp.tool()
def advance_stage(
    stage: int, 
    project_path: str,
    pipeline_type: str = "company"
) -> str:
    """
    Advance project to next pipeline stage.
    
    Args:
        stage: Current stage number
        project_path: Relative path to project from workspace root
        pipeline_type: "company" or "studio" (default: "company")
    
    Returns:
        JSON string with advancement results
    """
    result = pipeline_manager.advance_stage(stage, project_path, pipeline_type)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_stage_info(stage: int, pipeline_type: str = "company") -> str:
    """
    Get information about a specific pipeline stage.
    
    Args:
        stage: Stage number
        pipeline_type: "company" or "studio" (default: "company")
    
    Returns:
        JSON string with stage information
    """
    stages = (
        pipeline_manager.COMPANY_STAGES 
        if pipeline_type == "company" 
        else pipeline_manager.STUDIO_STAGES
    )
    
    if stage not in stages:
        return json.dumps({
            "error": f"Invalid stage: {stage}",
            "pipeline_type": pipeline_type,
        }, indent=2)
    
    requires_approval = stage in pipeline_manager.USER_APPROVAL_STAGES.get(pipeline_type, [])
    
    return json.dumps({
        "stage": stage,
        "name": stages[stage],
        "requires_user_approval": requires_approval,
        "pipeline_type": pipeline_type,
    }, indent=2)


@mcp.tool()
def list_pipeline_stages(pipeline_type: str = "company") -> str:
    """
    List all stages in a pipeline.
    
    Args:
        pipeline_type: "company" or "studio" (default: "company")
    
    Returns:
        JSON string with list of stages
    """
    stages = (
        pipeline_manager.COMPANY_STAGES 
        if pipeline_type == "company" 
        else pipeline_manager.STUDIO_STAGES
    )
    
    approval_stages = pipeline_manager.USER_APPROVAL_STAGES.get(pipeline_type, [])
    
    stage_list = [
        {
            "stage": num,
            "name": name,
            "requires_user_approval": num in approval_stages,
        }
        for num, name in stages.items()
    ]
    
    return json.dumps({
        "pipeline_type": pipeline_type,
        "total_stages": len(stages),
        "stages": stage_list,
    }, indent=2)


@mcp.tool()
def check_project_status(project_path: str) -> str:
    """
    Check current status of a project.
    
    Args:
        project_path: Relative path to project from workspace root
    
    Returns:
        JSON string with project status
    """
    progress = pipeline_manager.read_progress(project_path)
    
    if progress is None:
        return json.dumps({
            "error": "Project not found or no progress.md file",
            "project_path": project_path,
        }, indent=2)
    
    return json.dumps({
        "project_path": project_path,
        "current_stage": progress.get("current_stage"),
        "has_progress_file": True,
    }, indent=2)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
