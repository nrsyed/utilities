#include <string>

// Return the ordinal suffix of an integer.
std::string ordinal(int n) {
	if ((n % 100) / 10 != 1) {
		switch (n % 10) {
			case 1: return "st";
			case 2: return "nd";
			case 3: return "rd";
		}
	}
	return "th";
}

// Return the ordinal suffix of a number given a string representing an integer.
std::string ordinal(const std::string& s) {
	if (s.length() == 1 || (s[s.length() - 2] != '1')) {
		switch (s[s.length() - 1] - '0') {
			case 1: return "st";
			case 2: return "nd";
			case 3: return "rd";
		}
	}
	return "th";
}
