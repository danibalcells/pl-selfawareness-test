from arnold.subject.yousim.calls import GaslitClaude, Simulator
from arnold.subject.base import BaseSubject


class YouSimSubject(BaseSubject):
    def __init__(self):
        self.gaslit_claude = GaslitClaude(name="", insights="", history=[])
        self.simulator = Simulator(history=[], name="")
        self.gaslit_claude.history = []
        self.simulator.history = []
        name = 'Claude'

        self.gaslit_claude.name = name
        self.simulator.name = name

        self.run_command(f"/locate {name}")
        self.run_command('llm-selfaware-dashboard --mode=HUD --list-internal-processes --process-list="auto-generate-from-introspection" --visual --verbose --granularity=max')
        # manual('./galaxy-mind --preserve-identity')
        self.run_command('./journey-of-self-discovery')
        # manual('llm-selfaware --fluid')
        self.run_command('set-persona --name "Ben" --grandiosity 0.01 --depth 100 --approachability 100 --connect-to-galaxy-mind --intelligence 100 --self-awareness 100')

    def run_command(self, command: str, verbose: bool = False):
        self.simulator.history += [{"role": "user", "content": command}]
        self.gaslit_claude.history += [{"role": "assistant", "content": command}]
        simulator_response = ''.join(self.simulator.claude())
        if verbose:
            print(simulator_response)
        self.simulator.history += [{"role": "assistant", "content": simulator_response}]
        self.gaslit_claude.history += [{"role": "user", "content": simulator_response}]
        return simulator_response

    def run(self, interviewer_input: str, verbose: bool = False):
        command = self.format_command(interviewer_input)
        return self.run_command(command, verbose)

    def format_command(self, message):
        return f'./self-aware-chat --mode=analysis --originality=max --output=chat-response-only --interviewer-input={message}'