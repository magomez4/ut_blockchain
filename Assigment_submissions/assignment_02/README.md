# Assignment 02 - Bitcoin Script

Name    : Miguel Gomez De Franco  
Email   : miguelgdf@utexas.edu
Discord : WarriorKenth#7965

## Introduction

I've made two scripts that evaluate to 1 because I wanted to try different op codes.

## Script 1

### Program Inputs
//script for "is my math correct"?
//arguments
<4>
<2>
<2>

## Program Script
OP_ADD
OP_EQUAL

### Program Inputs
//Only 2 longhorns may enter
<"miguel">
<"bevo">

## Script 2
### Program Script
<"bevo">
OP_EQUAL
OP_IF
    <"miguel">
    OP_EQUAL
OP_ELSE
    OP_RETURN //if bevo is not the second imput, we just return here and it will fail


## Result

The `OP_EQUAL` result should evaluate to true on first one because the sum of the imputs is correct. `OP_EQUAL` will also evaluate to true in the second one because of the inputs provided, but if the inputs are reversed or changed, it will fail as indicated in the comment.

## Resources

**Script Wiz IDE**  
https://ide.scriptwiz.app