Commands to simulate an SMV model:
----------------------------------

1. Download nuXmv from here: https://nuxmv.fbk.eu/download.html
2. Enter the interative shell of nuXmv by executing the command:
   > nuXmv -int
3. Execute these commands:
   > set input_file example-1.smv
   > go
   > pick_state -v -r  -- this commands picks randomly an initial state of
                       -- the system
   > simulate -v -i -k 10 -- simulates the systems in an interactive
                          -- fashion for 10 steps


Commands to read an AIGER file:
--------------------------------

> nuXmv -int
> read_aiger_model -i example-1.aag
> go
> pick_state -v -r   -- now you can simulate the model like before
> simulate -v -i -k 10

build bollean model 

build_boolean
check_invar
