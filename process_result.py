import json
import pandas as pd

def process_result(result, llm_strategy, output_file):
        data = json.loads(result.extracted_content)
        print("Extracted items:", data)
        df = pd.DataFrame(data)
        df = df.map(lambda x: x if not isinstance(x, str) else x.encode('utf-8').decode('utf-8', errors='replace'))
                    
        if os.path.exists(output_file):
            old_df = pd.read_excel(output_file)
            combined_df = pd.concat([old_df, df], ignore_index=True)
        else:
            combined_df = df
                    
        combined_df.to_excel(output_file, index=False)
        print(f"Data has been successfully saved to {output_file}")

        llm_strategy.show_usage()