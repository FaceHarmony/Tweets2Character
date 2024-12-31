from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from Tweets2Character.utils.models import model_claude_sonnet

@CrewBase
class ProfilerCrew:
    """Profiler Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def profiler_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["profiler_specialist"],
            verbose=True,
            allow_delegation=False,
            llm = model_claude_sonnet
        )

    @task
    def profiler_specialist_task(self) -> Task:
        return Task(
            config=self.tasks_config["profiler_specialist_task"],
            verbose=True,
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Profiler Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
        )