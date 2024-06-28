Basic Utility AI
----------------

* A `reasoner` selects an `option` from a set of options, based on the
  logic set out below.
* Each `option` is assigned a set of `considerations`, which calculates
  a utility value based on circumstances. Typically, the utilities of
  all considerations of an option get multiplied to yield a final
  utility value.
* There are two basic ways of choosing an option:
  * Absolute value: Just choose the highest-scored option.
  * Relative value: Probability of option to be chosen = Utility of
    option / sum of utility of all options
* More complex selection schemes are possible, e.g. taking the top three
  options, and choosing between them based on relative utility.


Design Patterns for the Configuration of Utility-Based AI
---------------------------------------------------------

[Paper](https://course.khoury.northeastern.edu/cs5150f13/readings/dill_designpatterns.pdf)

Describes the Dual Utility Reasoner, and design patterns for
considerations used by it.


### Dual Utility Reasoner

* Considerations return a rank, a bonus, and a multiplier.
* Options are assigned a `rank` and a `weight`.
  * An option's `rank` is the maximum of the ranks of its
    considerations. Only the options with the highest rank will be
    considered.
  * An option's `weight` is the sum of the boni of its considerations
    times the product of the multipliers of its considerations.
* Conventions for ranks:
  * 0: Baseline (-5 to +5)
  * 10: Urgent (+5 to +15)
  * 20: To be done immediately
  * 1,000,000: Autonomous, uncontrollable actions


### Consideration patterns

* Option Validation
  * Opt Out: Conditionally block the option from being chosen by
    returning 0 (TODO: otherwise 1?). For an option to be eligible,
    the conditions of **all** Opt Out considerations must be false.
  * Opt In: The option should be chosen if at least one Opt In
    consideration condition is true. The option needs to have a
    default rank lower than the default option (e.g. -1). If the Opt
    In consideration's is true, a rank greater than the default option
    rank is returned.
* Execution History
  * Commit: Execute an option to its completion, even if the
    circumstances change so that the option would no longer be chosen.
    Once the option is chosen, this consideration will return a high
    rank until execution stops.
  * Inertia: Tend toward keeping up this behavior (unless something
    important happens) instead of going back to default behaviors.
    Once this option is chosen, this consideration will return a rank
    slightly below the rank at which the option was chosen.
  * Is Done: If this option is selected, and the execution is
    completed, return a multiplier of 0.
  * Cooldown: For some time after an option finishes executing, return
    a multiplier of 0.
  * Do Once: If this option has ever be selected, return a multiplier
    of 0.
  * One-Time Bonus: If this option has never been chosen, return a
    high rank or weight. Incompatible with Opt In.
  * Repeat Penalty: Start at a high rank, and decrease the rank by
    some amount each time that this option is executed.


### Further reading

* Game Programming Gems 8 (Dill 2010): Dual Utility Reasoner first
  discussed
* Dill 2011: Dual Utility Reasoner refined. More believable characters.
* Dill 2012: Dual Utility Reasoner refined
