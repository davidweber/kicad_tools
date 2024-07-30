<h3><pre>Usage: mk_kicad_symbol_lib.py &ltsymbol_input_directory&gt</h3>

The script generates output to stdout.  The intent is to pipe the output to the desired file.

For example:  If you have symbol files in a directory named symbols, use the following command to generate a library of those symbols.

  mk_kicad_symbol_lib.py symbols > my_symbol_lib.kicad_sym

The library is added to KiCad using the "File->Add Library" menu item and selecting the newly created "my_symbol_lib.kicad_sym" file.
</pre>
