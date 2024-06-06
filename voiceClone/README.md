Follow https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md
to install and setup openvoice

<!-- Inside voiceClone dir. -->
conda create -n openvoice python=3.9
conda activate openvoice
git clone git@github.com:myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .

then start server:
python3 main.py