import asyncio

from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

@magics_class
class Codilify(Magics):

    @cell_magic
    def codilify(self, parameters_s, cell):
        opts,args = self.parse_options(parameters_s,'le',mode='list')
        load = 'l' in opts
        edit = 'e' in opts
        filename = args[0]
        if load:
            with open(filename, "r") as f:
                src = "".join(f.readlines())
        else:
            src = str(cell)
            with open(filename, "w") as f:
                f.write(str(cell))
        ast_stmt = self.shell.compile.ast_parse(src)
        code = self.shell.compile(ast_stmt, "<magic-codilify>", "exec")        
        asyncio.ensure_future(self.shell.run_code(code, None))
        contents = f"%%codilify -l{'e'if edit else ''} {filename} \n"
        if edit:
            contents += src
        else:
            contents += "pass"
        self.shell.set_next_input(contents, replace=True)
        
    
def load_ipython_extension(ipython):
    ipython.register_magics(Codilify)
