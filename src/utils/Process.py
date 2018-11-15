import subprocess

class Process:

    @staticmethod
    def run(executable, params = [], cwd='.'):
        run_params  = [executable] + params
        result      = subprocess.run(run_params, cwd = cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return {
            "runParams" : run_params,
            "stdout"    : result.stdout.decode(),
            "stderr"    : result.stderr.decode(),
        }
