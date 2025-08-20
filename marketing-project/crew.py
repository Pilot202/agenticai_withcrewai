from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os, yaml
from fastapi import FastAPI, Request


os.environ["CREWAI_STORAGE_DIR"] = "./storage"
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7,api_key= gemini_api_key)

app = FastAPI()

base_dir = os.path.dirname(__file__)
config_path = os.path.join(base_dir, "config", "agents.yaml")
config_path2 = os.path.join(base_dir, "config", "tasks.yaml")

with open(config_path) as f:
    agents_config = yaml.safe_load(f)

with open(config_path2) as f:
    tasks_config = yaml.safe_load(f)


@CrewBase
class MarketingCrew():
    """Marketing crew"""



    @agent
    def marketing_manager(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['head_of_marketing'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), DirectoryReadTool(), FileWriterTool(), FileReadTool()],
            verbose=True,
            reasoning=True,
            allow_delegation=True,
            max_rpm=3,
            inject_date=True
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['content_creator_social_media'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), DirectoryReadTool(), FileWriterTool(), FileReadTool()],
            verbose=True,
            reasoning=True,
            allow_delegation=True,
            max_rpm=3,
            max_iter=2,
            inject_date=True
        )

    @agent
    def content_writer_blogs(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['content_writer_blogs'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), DirectoryReadTool(), FileWriterTool(), FileReadTool()],
            verbose=True,
            reasoning=True,
            allow_delegation=True,
            max_rpm=3,
            max_iter=2,
            inject_date=True
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['seo_specialist'],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), DirectoryReadTool(), FileWriterTool(), FileReadTool()],
            verbose=True,
            reasoning=True,
            max_rpm=3,
            max_iter=2,
            inject_date=True
        )

    @task
    def marketing_task(self) -> Task:
        return Task(config=self.tasks_config['market_research'], agent=self.marketing_manager())

    @task
    def prepare_marketing_strategy(self) -> Task:
        return Task(config=self.tasks_config['prepare_marketing_strategy'], agent=self.marketing_manager())

    @task
    def create_content_calendar(self) -> Task:
        return Task(config=self.tasks_config['create_content_calendar'], agent=self.content_creator())

    @task
    def prepare_post_drafts(self) -> Task:
        return Task(config=self.tasks_config['prepare_post_drafts'], agent=self.content_creator())

    @task
    def prepare_scripts_for_reels(self) -> Task:
        return Task(config=self.tasks_config['prepare_scripts_for_reels'], agent=self.content_creator())

    @task
    def content_research_for_blogs(self) -> Task:
        return Task(config=self.tasks_config['content_research_for_blogs'], agent=self.content_writer_blogs())

    @task
    def draft_blogs(self) -> Task:
        return Task(config=self.tasks_config['draft_blogs'], agent=self.content_writer_blogs())

    @task
    def seo_optimization(self) -> Task:
        return Task(config=self.tasks_config['seo_optimization'], agent=self.seo_specialist())

    def marketing_crew(self) -> Crew:
        return Crew(
            agents=[self.marketing_manager(), self.content_creator(), self.content_writer_blogs(), self.seo_specialist()],
            tasks=[
                self.marketing_task(), self.prepare_marketing_strategy(), self.create_content_calendar(),
                self.prepare_post_drafts(), self.prepare_scripts_for_reels(),
                self.content_research_for_blogs(), self.draft_blogs(), self.seo_optimization()
            ],
            memory=True
        )



if __name__ == "__main__":
    from datetime import datetime

    inputs = {
        "product_name": "AI Powered Excel Automation Tool",
        "target_audience": "Small and Medium Enterprises (SMEs)",
        "product_description": "A tool that automates repetitive tasks in Excel using AI, saving time and reducing errors.",
        "budget": "NIR, 50,000",
        "current_date": datetime.now().strftime("%Y-%m-%d"),
    }
    crew = MarketingCrew()
    crew.marketing_crew().kickoff(inputs=inputs)
    print("Marketing crew has been successfully created and run.")
