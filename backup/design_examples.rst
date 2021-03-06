Case study
==========

This chapter provides some example designs implemented using the experimental compiler.

First example developes and moving-average filter.

First three examples will interatively implement
DC-removal system. First design implements an simple fixed-point accumulator. Second one builds upon this and implements
moving average filter. Lastly multiple moving average filters are chained to form a DC removal circuit.

Second example is an FIR filter, with reloadable switchable taps ?

Third design example shows how to chain togather already exsisting Pyha blocks to implement greater systems.
In this case it is FSK receiver. This examples does not go into details.


Model based design is encouraged, where model is non-synthesisable code for simplest possible
implementation. Most often the model is implemented with a call to Numpy or Scipy (Python scientific computing libraries).
Model helps the testing process and can also serve as an documentation.

The ``model_main`` function is reserved for defining the model and ``main`` as the top level for synthesis. Note that the
``model_main`` is completely ignored for synthesis.

Notice how the ``model_main`` function works on lists, it gets all the inputs at once, this enabled vectorized
implementations. The ``main`` however works on single input, as is the hardware way.

Design flow
~~~~~~~~~~~

The Suggested design flow for Pyha designs is model based development with test-driven approach.
This means that the unit tests should be developed to assert the performance of the model.
For unit tests use the Pyha ``simulate`` functions, so that the same tests can be later executed for hardware models.

The last step is to implement the synthesizable code (``main``); development is greatly simplified
if enough unit tests were collected while developing the model.

.. todo:: Needs more info, make figure, fixed point?


.. note:: The following examples in this chapter tend to ignore the model and unit-testing part and go straight to the
    hardware implementation, since this is the focus of this chapter.


.. include:: moving_average.rst

.. include:: dc_removal.rst

.. include:: fsk_demodulator.rst

.. todo:: More stuff on results comparison..how good are they? etc. Yannic thinks this section will trigger
most of the questions in defence.



