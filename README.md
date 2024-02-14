# What’s this?
A quickly put together little Python script that enables you to postpone the due date of review notes and review cards as created by the [obsidian-spaced-repetition](https://www.stephenmwangi.com/obsidian-spaced-repetition/) plugin written by Stephen Mwangi ([st3v3nmw](https://github.com/st3v3nmw/obsidian-spaced-repetition)) for the [Obsidian](https://obsidian.md/) note taking/knowledge management app.

# Why?
This feature was [requested](https://github.com/st3v3nmw/obsidian-spaced-repetition/issues/798) in November 2023. Judging from the comments many dreaded they would not be able to keep up with their review queues during the winter festive period, and the request appeared to be supported by at least some users of the plugin. 

As of 14th Febuary 2024 this feature has not yet been implemented (see my [feature request (#798)](https://github.com/st3v3nmw/obsidian-spaced-repetition/issues/798)). Although got through the winter without too much of a backlog, sometimes I’d really like to have a weekend not “oriented around” my review queues or the fear that Monday’s review session will be brutal.

Since I don’t speak TypeScript, but desperately wanted a way to postpone review due dates, I thought I’d bridge the gap with this little Python script until the feature makes its way into the official [obsidian-spaced-repetition](https://www.stephenmwangi.com/obsidian-spaced-repetition/) plugin, which I’m sure will happen sooner or later.

# Okay, how do I use it?
Usage is simple but since the script was put together in the little free time I had you should **first be aware of the requirements** for use:
## Requirements
### Software
You must have Python (>3.8) installed on your system, although I think it should work with any Python3 version.
### Folder hierarchy and script placement
A picture is worth a thousand words. So I’ll start with that:
```
MyEmptyFolder/
├── MyVault/
└── obsidian_postponer.py
```
This means that:
1. you **MUST put** your Obsidian **Vault** (the directory of your vault) **inside an empty folder** (e.g. `MyEmptyFolder/MyVault`)
2. then you **MUST put** `obsidian_postponer.py` in `MyEmptyFolder` just at the same level as your `MyVault` folder is.

### Backup
Create a backup of your vault before processing it with the script!
# Sure can I use it already?
Yes you can. Follow the steps below:

>[!IMPORTANT] Close Obsidian before proceeding!

>[!WARNING] Make sure you didn’t skip the requirements!

1. Close Obsidian
2. Open a command line inside your `MyEmptyFolder`. Then ask Python to run the script like this, for example, to postpone **both your card AND note review due dates** by **10 days:**
```
python obsidian_postponer.py 10
```
You can postpone **cards only**:
```
python obsidian_postponer.py 10 -c
```
Or **notes only** too:
```
python obsidian_postponer.py 10 -n
```

>[!IMPORTANT] If you make a mistake…
>Example: you postponed everything by `100` days but you only wanted to postpone by `10`. Simply do another postpone of `-90` days. 

If you want to the script to tell you the above:
```
python obsidian_postponer.py --help
```
# Why the rigid hierarchy, though?
The script expects your Vault directory to be at the same level as the script itself. It will then traverse ALL directories further down relative to its ownlocation and work with any and all `.md` files it finds. 

**This can be cool:** if you have multiple Vault directories next to the script, it will postpone note/card review dates across all of those Vaults.

**This can be dangerous:** the script has no knowledge of Vaults. It simply looks for markdown (`.md`) files and processes them. If you run it in a folder that contains multiple Vaults all of them will be modified.

# Disclaimer
Run this script at your own risk, I make no guarantees. So make sure you **create a backup of your Vault first.**
