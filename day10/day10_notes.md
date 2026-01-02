
```
[.##.]   (3) (1,3) (2) (2,3) (0,2) (0,1)

[.##.]  = [0110]

(3)     = [0001]
(1,3)   = [0101]
(2)     = [0010]
(2,3)   = [0011]
(0,2)   = [1010]
(0,1)   = [1100]
```

----

```
[0110] = a[0001] ⨁ b[0101] ⨁ c[0010] ⨁ d[0011] ⨁ e[1010] ⨁ f[1100]
Solutions: (0,0,0,0,1,1), (0,1,0,1,0,0)
```

----

## Observations
- To find the least number of button presses to produce the light pattern, we need to find a linear combination of the available buttons such that each coefficient is a positive integer, as small as possible, and with as many coefficients set to 0 as possible.
- The linear combinations are under the ⨁ (xor) operation where, for instance, 3[0001] = [0001] ⨁ [0001] ⨁ [0001]. That is, we need the vector (a,b,c,d,e,f) with the least distance to the origin.
- However, no button will need pressed more than once, since pressing a button twice in a row reverts back to the initial state (also button presses commute with each other).
- Starting from an blank state `[......]` and pressing buttons to reach a target state `[.##.#..]` is equivalent to starting from the target state and pressing buttons to reach the blank state. That is, the same combination of buttons should work in both directions.

## Idea 1
- Given n buttons, form the n-bit binary number `00...0`. Each bit `i` will indicate whether the `i`-th button will be pressed (i.e. `1010` means only press the first and third buttons).
- Increment the number and test each combination of buttons until the first solution is found.
- This will guarantee the minimum number of presses since 


## Testing

### Combinations with 3 indicators (8 total)
[Presses] | [Combinations]
    0     |  000
    1     |  001 | 010 | 100
    2     |  011 | 101 | 110
    3     |  111

**Binary count order:**   000 -> 001 -> 010 -> 011 -> 100 -> 101 -> 110 -> 111
**Intended order:**       000 -> 001 -> 010 -> 100 -> 011 -> 101 -> 110 -> 111
                           0      1      2      4      3      5      6      7

### Combinations with 4 indicators (16 total)
[Presses] | [Combinations]
    0     |  0000
    1     |  0001 | 0010 | 0100 | 1000
    2     |  0011 | 0101 | 0110 | 1001 | 1010 | 1100
    3     |  0111 | 1011 | 1101 | 1110
    4     |  1111

**Binary count order:**   0000 -> 0001 -> 0010 -> 0011 -> 0100 -> 0101 -> 0110 -> 0111 -> 1000 -> 1001 -> 1010 -> 1011 -> 1100 -> 1101 -> 1110 -> 1111
**Intended order:**       0000 -> 0001 -> 0010 -> 0100 -> 1000 -> 0011 -> 0101 -> 0110 -> 1001 -> 1010 -> 1100 -> 0111 -> 1011 -> 1101 -> 1110 -> 1111
                            0       1       2       4       8       3       5       6       9       10      12      7       11      13      14      15

### Combinations with 5 indicators (32 total)
[Presses] | [Combinations]
    0     |  00000
    1     |  00001 | 00010 | 00100 | 01000 | 10000
    2     |  00011 | 00101 | 00110 | 01001 | 01010 | 01100 | 10001 | 10010 | 10100 | 11000
    3     |  00111 | 01011 | 01101 | 01110 | 10011 | 10101 | 10110 | 11001 | 11010 | 11100
    4     |  01111 | 10111 | 11011 | 11101 | 11110
    5     |  11111


