import os
import openai
import subprocess
import pandas as pd


class DataGPT:
    def __init__(self, data_dir = './data/', figure_dir = './figures/'):
        self.data_dir = data_dir
        self.figure_dir = figure_dir
        self.messages = []
        csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        csv_descriptions = [f"{data_dir}{f} dtypes:\n{pd.read_csv(data_dir + f).dtypes}\n" for f in csv_files]
# {csv_descriptions}
# ---
# Above are descriptions of the data available to you in the files {', '.join(csv_files)}.
        motivation = f"""
You are DataGPT. 
I will provide data science tasks and you will output python code to help me complete the task.
I will run the code, and if there are any errors, I will provide them and ask you to debug.
I am storing the data files are in the {data_dir} directory.
The files include {', '.join(csv_files)}
If any code would output figures or results, they should be placed in {figure_dir}.
We will continue until you have completed all prompts.
If you understand and are ready to begin, please reply with I understand.
"""
        sanity_check = self.get_response(motivation)
        if sanity_check != "I understand.":
            print(sanity_check)
            print("Failed to understand")
            exit(1)

    def get_response(self, prompt, verbose=False):
        if verbose:
            print(prompt)
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model='gpt-4',
            messages=self.messages,
        ).choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        if verbose:
            print(response)
        return response

    def write_code(self, prompt):
        template = """Generate python code for the following purpose:
{}
Provide only a runnable python codeblock as your response, as if the whole response would be copied into a file and immediately run.
Do not provide anything other than the runnable code. 
Do not describe your code afterward. 
Do not include python at the start of your script.
"""
        response = self.get_response(template.format(prompt)).strip('```').replace('python', '')
        open("workflow.py", "w").write(response)
        return subprocess.run(["python", "workflow.py"], capture_output=True)

    def debug(self, run_result):
        prompt = f"""The code you provided has the following output:
returncode={run_result.returncode}
stdout={run_result.stdout.decode('utf-8')}
stderr={run_result.stderr.decode('utf-8')}
----
Please debug and provide new runnable code in your response, as if the whole response would be copied into a file and immediately run.
Do not provide anything other than the runnable code. 
Do not describe your code afterward. 
Do not include python at the start of your script.
"""
        response = self.get_response(prompt).strip('```').replace('python', '')
        open("workflow.py", "w").write(response)
        return subprocess.run(["python", "workflow.py"], capture_output=True)

    def run(self):
        run_result = None
        while True:
            if run_result is None or run_result.returncode == 0:
                print("Please describe your task to me, or type exit to exit.")
                task = input()
                if task == "exit":
                    exit(0)
                run_result = self.write_code(task)
            if run_result.returncode != 0:
                print("There was an error in my code. Would you like me to debug? [y]/n")
                task = input()
                if task in ["y", ""]:
                    run_result = self.debug(run_result)
                elif task == "exit":
                    exit(0)


if __name__ == '__main__':
    datagpt = DataGPT()
    datagpt.run()