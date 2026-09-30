"""
Interface CLI en ligne de commande / API JSON pour exécuter les algorithmes Python
et faire le pont avec le serveur Web ou les tests automatisés.
"""

import sys
import io

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json
import traceback
from core.matrix_operations import matrix_add, matrix_subtract, matrix_multiply, matrix_divide, transpose, identity_matrix
from core.determinant import determinant
from core.inverse import inverse
from core.gaussian import row_echelon, rref
from core.solver import solve_system
from utils.validators import parse_matrix
from utils.formatter import format_matrix, format_number
from utils.storage import save_history_item, load_history, clear_history, delete_history_item

def handle_request(payload: dict) -> dict:
    action = payload.get("action")
    
    if action == "add":
        A = parse_matrix(payload["A"])
        B = parse_matrix(payload["B"])
        C, steps = matrix_add(A, B)
        dim_str = f"Matrice {len(A)}×{len(A[0])} + Matrice {len(B)}×{len(B[0])}"
        res_sum = f"Résultat : {len(C)}×{len(C[0])}"
        item = save_history_item(
            "Addition de matrices",
            {"A": A, "B": B},
            C,
            steps,
            action_type="add",
            formula="A + B",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": C, "steps": steps, "formatted": format_matrix(C), "history_item": item}
        
    elif action == "subtract":
        A = parse_matrix(payload["A"])
        B = parse_matrix(payload["B"])
        C, steps = matrix_subtract(A, B)
        dim_str = f"Matrice {len(A)}×{len(A[0])} − Matrice {len(B)}×{len(B[0])}"
        res_sum = f"Résultat : {len(C)}×{len(C[0])}"
        item = save_history_item(
            "Soustraction de matrices",
            {"A": A, "B": B},
            C,
            steps,
            action_type="subtract",
            formula="A - B",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": C, "steps": steps, "formatted": format_matrix(C), "history_item": item}
        
    elif action == "multiply":
        A = parse_matrix(payload["A"])
        B = parse_matrix(payload["B"])
        C, steps = matrix_multiply(A, B)
        dim_str = f"Matrice {len(A)}×{len(A[0])} × Matrice {len(B)}×{len(B[0])}"
        res_sum = f"Résultat : {len(C)}×{len(C[0])}"
        item = save_history_item(
            "Multiplication de matrices",
            {"A": A, "B": B},
            C,
            steps,
            action_type="multiply",
            formula="A × B",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": C, "steps": steps, "formatted": format_matrix(C), "history_item": item}

    elif action == "divide":
        A = parse_matrix(payload["A"])
        B = parse_matrix(payload["B"])
        C, steps = matrix_divide(A, B)
        dim_str = f"Matrice {len(A)}×{len(A[0])} ÷ Matrice {len(B)}×{len(B[0])}"
        res_sum = f"Résultat : {len(C)}×{len(C[0])}"
        item = save_history_item(
            "Division de matrices",
            {"A": A, "B": B},
            C,
            steps,
            action_type="divide",
            formula="A ÷ B",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": C, "steps": steps, "formatted": format_matrix(C), "history_item": item}
        
    elif action == "transpose":
        A = parse_matrix(payload["A"])
        A_T, steps = transpose(A)
        dim_str = f"Matrice {len(A)}×{len(A[0])}"
        res_sum = f"Résultat : {len(A_T)}×{len(A_T[0])}"
        item = save_history_item(
            "Transposée d'une matrice",
            {"A": A},
            A_T,
            steps,
            action_type="transpose",
            formula="Aᵀ",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": A_T, "steps": steps, "formatted": format_matrix(A_T), "history_item": item}
        
    elif action == "determinant":
        A = parse_matrix(payload["A"])
        det, steps = determinant(A)
        dim_str = f"Matrice {len(A)}×{len(A[0])}"
        res_sum = f"Det(A) = {format_number(det)}"
        item = save_history_item(
            "Déterminant d'une matrice",
            {"A": A},
            det,
            steps,
            action_type="determinant",
            formula="Det(A)",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": det, "formatted": format_number(det), "steps": steps, "history_item": item}
        
    elif action == "inverse":
        A = parse_matrix(payload["A"])
        inv, steps, is_inv = inverse(A)
        dim_str = f"Matrice {len(A)}×{len(A[0])}"
        res_sum = f"Résultat : {len(A)}×{len(A)}" if is_inv else "Non inversible (Det = 0)"
        item = save_history_item(
            "Inversion de matrice",
            {"A": A},
            inv,
            steps,
            action_type="inverse",
            formula="A⁻¹",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {
            "success": True,
            "result": inv,
            "is_invertible": is_inv,
            "steps": steps,
            "formatted": format_matrix(inv) if inv else None,
            "history_item": item
        }
        
    elif action == "identity":
        n = payload.get("n")
        if not n and "A" in payload:
            A = parse_matrix(payload["A"])
            n = len(A)
        else:
            n = int(n or 3)
        I_mat, steps = identity_matrix(n)
        dim_str = f"Dimension {n}×{n}"
        res_sum = f"Résultat : {n}×{n}"
        item = save_history_item(
            f"Matrice Identité I_{n}",
            {"n": n, "A": payload.get("A") or I_mat},
            I_mat,
            steps,
            action_type="identity",
            formula=f"I_{n}",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": I_mat, "steps": steps, "formatted": format_matrix(I_mat), "history_item": item}
        
    elif action == "ref":
        A = parse_matrix(payload["A"])
        ref_matrix, step_objs = row_echelon(A)
        dim_str = f"Matrice {len(A)}×{len(A[0])}"
        res_sum = f"Forme REF"
        item = save_history_item(
            "Forme Échelonnée (REF)",
            {"A": A},
            ref_matrix,
            step_objs,
            action_type="ref",
            formula="REF(A)",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": ref_matrix, "steps": step_objs, "formatted": format_matrix(ref_matrix), "history_item": item}
        
    elif action == "rref":
        A = parse_matrix(payload["A"])
        rref_matrix, step_objs = rref(A)
        dim_str = f"Matrice {len(A)}×{len(A[0])}"
        res_sum = f"Forme RREF"
        item = save_history_item(
            "Forme Échelonnée Réduite (RREF)",
            {"A": A},
            rref_matrix,
            step_objs,
            action_type="rref",
            formula="RREF(A)",
            dimensions=dim_str,
            result_summary=res_sum
        )
        return {"success": True, "result": rref_matrix, "steps": step_objs, "formatted": format_matrix(rref_matrix), "history_item": item}
        
    elif action == "solve_system":
        A = parse_matrix(payload["A"])
        B = [float(x) for x in payload["B"]]
        sol_type, vec, aug_final, step_objs, explanation = solve_system(A, B)
        dim_str = f"Système {len(A)} équations × {len(A)} inconnues"
        
        if sol_type == "UNIQUE" and vec:
            res_sum = "Solution unique : " + ", ".join([f"x{i+1}={format_number(v)}" for i, v in enumerate(vec)])
        elif sol_type == "INFINITE":
            res_sum = "Infinité de solutions"
        else:
            res_sum = "Aucune solution (Incompatible)"
            
        item = save_history_item(
            "Résolution d'un système linéaire",
            {"A": A, "B": B},
            {"type": sol_type, "vector": vec, "explanation": explanation},
            step_objs,
            action_type="solve_system",
            formula="AX = B",
            dimensions=dim_str,
            result_summary=res_sum,
            solution_type=sol_type
        )
        return {
            "success": True,
            "solution_type": sol_type,
            "vector": vec,
            "formatted_vector": [format_number(x) for x in vec] if vec else None,
            "final_augmented": aug_final,
            "formatted_augmented": format_matrix(aug_final),
            "steps": step_objs,
            "explanation": explanation,
            "history_item": item
        }
        
    elif action == "get_history":
        return {"success": True, "history": load_history()}
        
    elif action == "delete_history_item":
        item_id = payload.get("id")
        updated = delete_history_item(item_id)
        return {"success": True, "history": updated}

    elif action == "clear_history":
        clear_history()
        return {"success": True, "history": []}
        
    else:
        raise ValueError(f"Action inconnue : '{action}'")

def main():
    try:
        if len(sys.argv) > 1:
            raw_input = sys.argv[1]
        else:
            raw_input = sys.stdin.read()
            
        payload = json.loads(raw_input)
        res = handle_request(payload)
        print(json.dumps(res, ensure_ascii=False))
    except Exception as e:
        err_res = {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(err_res, ensure_ascii=False))

if __name__ == "__main__":
    main()
