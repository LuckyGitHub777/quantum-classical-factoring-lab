# Classical Factoring — Learning Lab

An offline Python exercise in the **classical** post-processing surrounding Shor's factoring algorithm. It factors only small integers, with bounded input and repeatable examples; it does **not** run quantum order finding or break real RSA keys.

## Try it

```bash
python shor_factor_demo.py 21
python -m unittest discover -s tests -v
```

Python 3.10+; no third-party packages, online services or privileged access required. The bundled tests cover small factors, prime inputs, error bounds and honest command-line messaging.

**Use and rights:** Educational source is publicly viewable. No redistribution or derivative-use license is granted by this repository. The demonstration does not establish real-world cryptographic capability. `MANIFEST.sha256` records the released files.
