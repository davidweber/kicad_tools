<h3><pre>Usage: mk_kicad_symbol_lib.py &ltsymbol_input_directory&gt</h3>

This script generates output to stdout.  The intent is to redirect the output to the desired file.

For example:  If you have symbol files in a directory named <b>symbols</b>, use the following command to generate a library of those symbols.

  <pre>mk_kicad_symbol_lib.py symbols > my_symbol_lib.kicad_sym</pre>

The library is added to KiCad using the <b>"File->Add Library"</b> menu item and selecting the newly created <b>"my_symbol_lib.kicad_sym"</b> file.

This script was designed to run from the Linux command-line, but should also run on Mac's as described above.  To run from Windows terminal window:
<pre>python mk_kicad_symbol_lib.py</pre>
