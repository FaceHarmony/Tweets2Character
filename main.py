from pathlib import Path
from crewai.flow.flow import listen, start, Flow, router, or_
from dotenv import load_dotenv
import argparse
from Tweets2Character.profiler_crew.profiler_crew import ProfilerCrew
from Tweets2Character.utils.validate import validate_json
import json

load_dotenv()

    
def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

class ProfileUserFlow(Flow):

    def __init__(self, name: str, tweets: str, basicUserInfo: str, output_json_path: str):
        super().__init__()
        self.profiler = ProfilerCrew().crew()
        self.basicUserInfo = basicUserInfo
        self.name = name
        self.tweets = tweets
        self.output_json_path = output_json_path
        self.profiler_result = None

    @start()
    def profile_user(self):
        result = self.profiler.kickoff(inputs={"tweets": self.tweets, "name": self.name, "basicUserInfo": self.basicUserInfo})        
        if isinstance(result.raw, str) and result.raw.startswith('```json'):
            json_str = result.raw.replace('```json', '').replace('```', '').strip()
            self.profiler_result = json.loads(json_str)
        else:
            self.profiler_result = result

    @listen(profile_user)
    def verify_json(self):
        if validate_json(self.profiler_result):
            content = json.dumps(self.profiler_result, indent=4) if isinstance(self.profiler_result, dict) else self.profiler_result
            write_file(self.output_json_path, content)        
        else:
            print("JSON is not valid")

# Add argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description='Profile a user based on their tweets and basic info')
    parser.add_argument('--name', type=str, required=True, help='Name of the user to profile')
    parser.add_argument('--tweets-file', type=str, required=True, help='Path to the file containing tweets')
    parser.add_argument('--user-info-file', type=str, default='', help='Path to the file containing basic user info')
    parser.add_argument('--output-path', type=str, default='./output_profile.json', help='Path where the output JSON will be saved')
    return parser.parse_args()

# Replace the bottom portion with argument handling
if __name__ == "__main__":
    args = parse_args()
    
    with open(args.tweets_file, 'r') as f:
        tweets = f.read()
    
    if args.user_info_file:
        with open(args.user_info_file, 'r') as f:
            basicUserInfo = f.read()
    else:
        basicUserInfo = ""
    
    flow = ProfileUserFlow(
        name=args.name,
        tweets=tweets,
        basicUserInfo=basicUserInfo,
        output_json_path=args.output_path
    )
    
    results = flow.kickoff()
