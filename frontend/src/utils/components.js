import { getApiUrl } from "./config";

export class ComponentData {
    id = 0;
    name = "";
    description = "";
    iconUrl = "";
}

export async function fetchComponents() {
    const result = [];
    const data = await fetch(
        getApiUrl("components/"),
    )

    for (let comp of await data.json()) {
        const c = new ComponentData();
        c.id = comp.id;
        c.name = comp.name;
        c.description = comp.description;
        c.iconUrl = "/component.jpeg";
        result.push(c);
    }

    return result;
}