## What is this?

Code and data for analyzing the Countdown TV show numbers game. Full info at hdtx.io/countdown.

## Data files

* `countdown-data.7z`: this contains a series of text files, one for each large numbers count (so `stats0.txt` is data for games with 0 large numbers and 6 small,  `stats1.txt` is data for games with 1 large number and 5 small, and so on). The first line is all canonical games with their respective frequency, in a compressed representation format. The following lines have information for one game in each. In order (separator is a '#'): numbers involved in that game, frequency of that game, accumulated frequency of solvable games since the beginning of the file, Python dict representation where the key is the target number and the value is a solution in RPN notation.
* `countdown-csv.7z`: contains one compressed CSV file just with frequency and solvability (yes/no -> 1/0) information for each game and target between 90 and 1009.

## Author

**Henrique Daitx**
- <https://github.com/hdtx>

## License

Open sourced under the [MIT license](LICENSE.md).
