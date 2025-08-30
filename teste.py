def trata_float(string : str) -> str:
    try:
        valor = float(string)
    except ValueError:
        valor = string[::-1].replace(',', '.', 1)[::-1]
    return f"{round(float(valor),2):.2f}"

print(trata_float(''))