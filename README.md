# pype

Use Python snippets with your Unix workflows

# Example Usage

Assuming you've aliased `pype`:

```bash
# 103214654_artist_feat_some_other_artist -> "artist feat some other artist"
ls *.wav                                                                                          |
  pype --map --import re -- '"{} \"{}\"".format(_, re.sub(r"^\d+_", "", _))'                      |
  pype --map --import re -- '"{} {}".format(_.split(" ")[0], re.sub(r"_", " ", _.split(" ")[1]))' |
  xargs -n2 cp -v
```
