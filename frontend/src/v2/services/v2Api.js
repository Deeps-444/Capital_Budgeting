import axios from "axios";

const v2Api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 120000,
});

export async function extractProjectDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await v2Api.post("/extract-document", formData);

  return response.data;
}

export async function predictProject(payload) {
  const response = await v2Api.post("/predict", payload);
  return response.data;
}


export async function researchProjectAssumptions(project) {
  const response = await v2Api.post("/research-assumptions", {
    project,
  });

  return response.data;
}

export default v2Api;
