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
