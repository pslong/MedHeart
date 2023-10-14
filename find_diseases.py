ori_map = {
  "疾病1": ["症状A", "症状B", "症状C", "症状D", "症状E", "症状F"],
  "疾病2": ["症状A", "症状B", "症状C", "症状E", "症状F"],
  "疾病3": ["症状A", "症状B", "症状C", "症状D",],
  "疾病4": ["症状C", "症状B", "症状E", "症状F"],
}

symptoms = ["症状A", "症状B"]

def findPossibleDisease(ori_map: dict, symptoms: list) -> dict:
    possible_disease = []
    possible_symptoms = {}

    for disease, symptoms_of_disease in ori_map.items():
        if all(symptom in symptoms_of_disease for symptom in symptoms):
            possible_disease.append(disease)
            for sympt in symptoms_of_disease:
                if sympt not in symptoms:
                    possible_symptoms[sympt] = possible_symptoms.get(sympt, 0) + 1
    n = len(possible_disease)
    ask_diseases = {}
    for k in possible_symptoms:
        if possible_symptoms[k]<n:
            ask_diseases[k]=possible_symptoms[k]

    return possible_disease,ask_diseases

result = findPossibleDisease(ori_map, symptoms)

print(result)