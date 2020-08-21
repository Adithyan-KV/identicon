# Identicon
Generate random Identicon avatars (like the ones github uses) using python.

## Examples
![Some example Identicons](/demo.png)

## How it works
Identicons are generated based on usernames. The hash values of the username are used for deterministically generating identicons so the same username always gets the same Identicon. 
Theoretically there are over 3 million possible variations of identicons and it is highly unlikely that any two users having different usernames will get 
the same Identicon.

## Dependancies
The code uses numpy for manipulating the pixel data matrices for the images and PIL for writing and manipulating images.
```
pip install numpy
pip install pillow
```

## Usage
Clone the repo and from its contents copy paste the *identicons.py* file to your working directory. After that Identicons can be imported as a module and used.
*( yes it is very shabby, but no one is ever going to use this stuff, Might upload it to PyPi if it ever gets half competent and
i feel like making the process more streamlined )*

```
import identicons

#generates a 256x256 identicon for username and save image to current working directory
identicons.generate('username',256)
```

Doesn't allow for any format other than PNG right now.
Doesn't support writing to a different path as of now.
Doesn't allow to access the image data instead of writing it out as of now.

These are all trivial fixes and I'll prolly fix them soon.
