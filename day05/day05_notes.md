## Initial attempts at `Part2()`
```py
    # Step 1: Record the length of each (inclusive) ID range (not considering overlaps).
    id_range_lengths:dict[tuple, int] = dict()
    for fresh_range in fresh_id_ranges:
        id_range_lengths[fresh_range] = fresh_range[1] - fresh_range[0] + 1
    
    # Step 2: Check for full overlaps.
    fresh_id_ranges_with_full_overlaps_removed = fresh_id_ranges.copy()
    skip_ranges:list[tuple] = []
    for i, this_range in enumerate(fresh_id_ranges):
        # If we've marked this range for skipping in an earlier iteration, skip to the next range.
        if this_range in skip_ranges:
            continue
        
        # Compare this range to all subsequent ranges to check if this range fits entirely inside another.
        for compare_range in fresh_id_ranges[i+1:]:
            
            #   |<---------- this_range --------->|     (`compare_range` inside `this_range`)
            #        |<--- compare_range --->|
            if this_range[0] <= compare_range[0] and compare_range[1] <= this_range[1]:
                # If a full overlap is found, remove the smaller range (`compare_range`) from both
                #  the ID list and the length dict.
                fresh_id_ranges_with_full_overlaps_removed.remove(compare_range)
                id_range_lengths.pop(compare_range)
                
                # Mark the removed range for skipping when encountered later in the loop.
                skip_ranges.append(compare_range)
            
            #        |<---- this_range --->|            (`this_range` inside `compare_range`)
            #   |<-------- compare_range -------->|
            elif compare_range[0] <= this_range[0] and this_range[1] <= compare_range[1]:
                # If a full overlap is found, remove the smaller range (`this_range`) from both
                #  the ID list and the length dict.
                fresh_id_ranges_with_full_overlaps_removed.remove(this_range)
                id_range_lengths.pop(this_range)
                
                # Since this range has been removed, stop comparing it to later ranges.
                # If any ranges later in the list are overlapped by `this_range`, they will be 
                #  overlapped by `compare_range` as well, so they will be removed later.
                break
    
    fresh_id_ranges = fresh_id_ranges_with_full_overlaps_removed
    
    # Step 3: Check for partial overlaps.
    fresh_id_ranges_with_partial_overlaps_removed = fresh_id_ranges.copy()
    skip_ranges:list[tuple] = []
    for i, this_range in enumerate(fresh_id_ranges):
        # If we've marked this range for skipping in an earlier iteration, skip to the next range.
        if this_range in skip_ranges:
            continue
        
        # Compare this range to all subsequent ranges to check if any part of this range overlaps with another.
        # If so, merge these two ranges into one and replace the `compare_range` in the list with the combined range.
        # This way, any additional ranges that overlap `this_range` will be caught later when `compare_range` is checked,
        #  since they must ....
        for compare_range in fresh_id_ranges[i+1:]:
            if (
                this_range[0] < compare_range[0] < this_range[1] < compare_range[1] or
                compare_range[0] < this_range[0] < compare_range[1] < this_range[1]
            ):
              ...  
```

## Scratch work
```
3-9
10-14
16-20
12-18
23-35
30-40
25-31


[this_range]
111-199
[compare_range]
100-200


4-7
3-8
5-6
1-10
2-9

3-8
5-6
1-10
2-9

3-8
1-10
2-9

1-10
2-9


this_range[0]------------------------this_range[1]
                comp_range[0]-----------------------comp_range[1]


303668309196282 - low
303668309196281 - low
400013897297828 - ?
361615643045064 - ?
361615643045059
```

### Render visual example of range overlaps
```py
n = '3-9, 7-13, 16-20, 11-16, 13-18, 2-7, 19-26, 1-4'
m = [tuple(map(int, x.split('-'))) for x in n.split(', ')]
for t in m: print(f'{"▢"*(t[1]-t[0]+1):>{t[1]}}')
```