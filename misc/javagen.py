
from yaml import load, CLoader


def gen(filename: str) -> None:
    with open(filename, "r") as f:
        data = load(f, Loader=CLoader)

    print("var rules = List.of(")
    for group in data["rules"]:
        rule_comma = "," if group != data["rules"][-1] else ""
        verbs = ", ".join(f'"{x}"' for x in group["verbs"])
        apiGroup = group["apiGroups"][0]

        print('    new V1PolicyRule()')
        print(f'        .apiGroups(List.of("{apiGroup}"))')
        print(f'        .resources(List.of(')
        for resource in group["resources"]:
            comma = "," if resource != group["resources"][-1] else ""
            print(f'            "{resource}"{comma}')
        print("        ))")
        print(f"        .verbs(List.of({verbs})){rule_comma}")
    print(");")


if __name__ == "__main__":
    gen("cluster-role.yaml")
