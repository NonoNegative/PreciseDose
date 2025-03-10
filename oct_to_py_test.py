from oct2py import Oct2Py
oc = Oct2Py()


script= "function drug_dose=drugdose(C_p, CL, tau, F)\n" \
        "    drug_dose=(C_p.*CL.*tau)./F"\
        "end"

with open("myScript.m","w+") as f:
    f.write(script)

oc.myScript(10, 10, 10, 2)