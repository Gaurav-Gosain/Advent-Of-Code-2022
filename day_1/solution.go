/*
? Usage: go run solution.go input/input.txt
* Output:

Part 1:  70720
Part 2:  207148

*/

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func main() {
	input, _ := ioutil.ReadFile(os.Args[1])
	lines := strings.Split(string(input), "\n\n")
	data := make([]int, len(lines))

	for _, line := range lines {
		split := strings.Split(line, "\n")
		total := 0
		for _, num := range split {
			num, _ := strconv.Atoi(num)
			total += num
		}
		data = append(data, total)
	}

	//? sort sum_list
	for i := 0; i < len(data); i++ {
		for j := i + 1; j < len(data); j++ {
			if data[i] < data[j] {
				data[i], data[j] = data[j], data[i]
			}
		}
	}

	//? Part 1
	fmt.Println("Part 1: ", data[0])

	//? Part 2
	part_2 := 0
	for i := 0; i < 3; i++ {
		part_2 += data[i]
	}
	fmt.Println("Part 2: ", part_2)
}
