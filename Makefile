PYTHONPATH = PYTHONPATH="/home/$${USER}/ATB:/home/$${USER}/ATB-Dependencies"

test:
	$(PYTHONPATH) python fragment_dihedral.py

fragment_generator:
	$(PYTHONPATH) python fragment_generator.py

tables:
	$(PYTHONPATH) python latex_table.py
