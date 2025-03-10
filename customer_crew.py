import os
import json
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import openai
from openai import OpenAI
from langchain_openai import ChatOpenAI
from crewai_tools import PDFSearchTool, JSONSearchTool



os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

GPT_MODEL = LLM(
    model="anthropic/claude-3-5-sonnet-20241022",
    temperature=0
)

#GPT_MODEL = "gpt-3.5-turbo-0125"

openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key = openai.api_key,
)

# Instantiate tools
hr_policies = PDFSearchTool(pdf="../HR_Policies.pdf")

accountant = JSONSearchTool(json_path="memory/accountant/baseline.json")
techical_support = JSONSearchTool(json_path="memory/technical_support/baseline.json")
marketing_manager = JSONSearchTool(json_path="memory/marketing_manager/baseline.json")
human_resource_manager = JSONSearchTool(json_path="memory/human_resource_manager/baseline.json")

# manager_llm
# manager_llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

@CrewBase
class CustomerServiceCrew:
    """Customer Service crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def accounting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['accounting_agent'],
            allow_delegation=False,
            verbose=True,
            llm=GPT_MODEL,
            tools=[accountant],
        )
    
    @agent
    def technical_support_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['technical_support_agent'],
            allow_delegation=False,
            verbose=True,
            llm=GPT_MODEL,
            tools=[techical_support],
        )
    
    @agent
    def marketing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['marketing_agent'],
            allow_delegation=False,
            verbose=True,
            llm=GPT_MODEL,
            tools=[marketing_manager],
        )
    
    @agent
    def human_resource_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['human_resource_agent'],
            allow_delegation=False,
            verbose=True,
            tools=[hr_policies, human_resource_manager],
            llm=GPT_MODEL,
        )
    
    # manager_agent
    manager = Agent(
            role ="Project Manager",
            goal=" Efficiently manage the crew and ensure high-quality task completion",
            backstory=" You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
            allow_delegation=True,
            verbose=True
        )
    
    @task
    def customer_query(self) -> Task:
        return Task(
            config=self.tasks_config['customer_query'],
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the CustomerServiceCrew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.hierarchical,
            #manager_agent=self.manager,
            manager_llm = GPT_MODEL,
            verbose=True, 
        )
    
    