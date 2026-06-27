# PinPointer

PinPointer is an error measurement system that enables motor behavior researchers to quickly and easily calculate 
the error (x-axis, y-axis, and radial error distances) between an object and target location (e.g., a golf ball 
and hole). PinPointer automatically calculates statistical measures for each error type which can be exported for 
additional analysis.

Please see the Releases tab to the right for the most recent Windows and MacOS executables.

For more details, or if you use PinPointer in your work, please reference \[1\].

\[1\] TODO once published

## How measures are calculated

PinPointer calculates a _scaling factor_, or the linear transformation of the distance between two points in an image (e.g., the target and implement) and their real-world distance. For each image, PinPointer calculates the error along the x-axis ($\Delta x$), error along the y-axis ($\Delta y$), and radial error using the following formulas:

$$scaling\ factor = \frac{dist_{real\ world}}{dist_{image}}$$
$$ \Delta x = (x_{target} - x_{implement}) \dot (scaling\ factor) $$
$$ \Delta y = (y_{target} - y_{implement}) \dot (scaling\ factor) $$
$$ Radial\ Error = \sqrt{\Delta x^2 + \Delta y^2} $$

## Copyright Information

Copyright 2025 SFSU PHAST Lab

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
