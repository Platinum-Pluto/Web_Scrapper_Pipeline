# Overview  
This project's aim is to gather and structure data from unstructured data from websites. My idea is to make it fully open source and free, so instead of using API keys, which nowadays are quite affordable, I wanted to combine `ollama` and `crawl4ai` together so that students and people who want an easier solution to gather important data from unstructured and structured data from websites can benefit from this.  

Since most LLM models work quite well with English, this code first translates the webpage to English and then gathers the data from it.  

---

# Installation (For Windows)  

- **Step - 1**  
   ```bash
   pip install crawl4ai
   ```
- **Step - 2**    
    ```bash
   crawl4ai-setup
   ```
- **Step - 3**    
    ```bash
   crawl4ai-doctor
   ```

---

# Google Colab  
For Google Colab, it uses `ollama` and `crawl4ai`.  
It's far from being perfect yet, but if you have a low-end laptop or PC, then with the right choice of LLM model and configurations, this is a good choice to get started with something instead of collecting data manually.  

Run each cell separately. However, keep in mind that when executing the cell containing:  
```bash
!ollama run modelName
```
You have to **interrupt the execution** of this cell when the `::` kind of loading pops up and then keep on executing the other cells without any worries.  

Also, set:  
```python
model_name = "The available ollama model that you would like to use"
```
Also edit:  
```bash
!ollama run TheModelNameAvailable
```
In the output file, set the location of your output file:  
```python
output_file = "Set the location of your output file"
```
For website URLs, add the websites that you would like to extract data from:  
```python
website_url = [
    "",
    "",
    ""
]
```
Then for the `INSTRUCTION`, make it concise.  

You can edit the `CompanyInfo` to a schema your data is going to be like.  

Adjust the values as you see fit for all the configurations.  
