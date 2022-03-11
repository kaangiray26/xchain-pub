# xchain 🖇
Encrypt Files with Shared Keys 

## Installation
Please follow the instructions in [this website](https://pygobject.readthedocs.io/en/latest/getting_started.html) for installing PyGObject according to your system. After that you can use the following instructions to make sure you have the necessary dependencies.
```
git clone https://github.com/kgbzen/xchain-pub.git
cd xchain-pub
python -m pip install -r requirements.txt
```

## Usage
```
python main.py
```

## What does it do?
**xchain** encrypts files and splits them into multiple keys, so that the original file can only be reproduced if all keys are gathered together.

## How?
**xchain** generates cryptographically secure random bit sequences and uses the **XOR** operation to create a block of sequences.  
So, the original file becomes the result, when the block of sequences are XOR-ed together.

## But, how? (visually)
Consider the following schema:

```
01010101101110 ($)

--------------

11111111111111 (£1)
01010101101010 (#11)
10101010010101 (#12)

--------------

10101010010001 (£2)
01010110101011 (#21)
11111100111010 (#22)

--------------

==> £1 is created from XOR(#11, #12)
==> £2 is created from XOR(#21, #22)
==> $ is created from XOR(£1, £2)
<=> $ is created from XOR(XOR(#11, #12), XOR(#21, #22))
```

This way we have split the original data in 4 distinct bit sequences. The original data can only be reproduced if the 4 bit sequences are available. We can iteratively or recursively create a random key, xor it with the last key in the list, remove the last key in the list, and add our random key and the result from the xor operation to the key list. This way, we can create longer xor chains to reach the desired number of keys.
