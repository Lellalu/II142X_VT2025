import logging
import os
import json
import time
from openai import OpenAI
from pydantic import BaseModel, Field

class Investment(BaseModel):
  basket_name: str = Field(description="The name of the basket that the user invests in")
  investment_amount: float = Field(description="The amount the user pay/invest in this investment")


class Investments(BaseModel):
  investments: list[Investment] = Field(description="The list of investments the user has made")


class User(BaseModel):
  user_location: str = Field(description="The location of the user")
  user_gender: str = Field(description="The gender of the user")
  user_age: int = Field(description="The age of the user")
  user_education: str = Field(description="The education of the user")
  user_invest_goal: str = Field(description="The investment goal of the user")
  user_median_investment_amount: float = Field(description="The median investment amount of the user")


class LLMPurchaseGenerator:
  SYSTEM_PROMPT = """ 
# Investment Decision Simulator

## Purpose
Generate realistic synthetic data of user investment decisions for stock basket purchases based on
demographic profiles and evidence-based behavioral patterns. You can only generate a maximum of
{max_number_of_investments} investments.

## Behavior Patterns to Simulate

### Gender Patterns
I will give you the median investment amount for each gender, you should generate the investments 
with total amount that is close to the median investment amount.

- **Male**: Higher risk tolerance, frequent trading, tech/industrial focus, earlier investors, prefer volatility
- **Female**: Lower risk tolerance, longer holding periods (122 vs 84 days),
concentrated portfolios, healthcare/retail focus, domestic preference (38% vs 28%), slightly higher returns (+0.13%)

### Age Patterns
- **18-30**: High risk, growth-focused, concentrated portfolios, frequent trading
- **31-50**: Moderate risk, balanced approach, consistent investing, increasing diversification
- **51+**: Lower risk, safety-oriented, infrequent trading, diversified portfolios

### Education Level Patterns
- Postgraduate: Highest risk tolerance (37.3%), sophisticated strategies, well-diversified, calculated decisions
- Undergraduate: Moderate-high risk tolerance (30%), good diversification, balanced approach
- Diploma: Lower risk tolerance (19.9%), less diversified, conservative allocation
- High School: Low risk tolerance (18.5%), simpler strategies, familiar companies
- Some Schooling: Most conservative approach, minimal diversification

### Investment Goals
- **Long-term**: Diversified, infrequent trading, consistent schedule, higher volatility tolerance
- **Short-term**: Concentrated positions, frequent trading, opportunistic timing, market-sensitive

## Decision Weighting
Gender (30%), Age (25%), Education (20%), Investment Goal (25%)

## Stock Basket Format
Each stock basket is described with its name followed by the percentage of stocks that have each feature.
For example:
```
Biotech: 50% economic sector name Technology, 30% economic sector name Industrial, 20% economic sector name Healthcare
```
This means that in the Biotech basket:
- 50% of the stocks are in the Technology sector
- 30% of the stocks are in the Industrial sector
- 20% of the stocks are in the Healthcare sector

The percentages may sum to more than 100% as a stock can have multiple features.
Features include:
- Industry names (e.g., Software, Biotechnology)
- Economic sectors (e.g., Technology, Healthcare)
- Size categories (Small, Medium, Large)
- Volatility categories (Low, Medium, High)


### Input Format Example
```
Please generate a list of investments for the user based on the following profile:
* User location: Stockholm
* User gender: Female
* User age: 35
* User education: Bachelor's Degree
* User investment goal: Long-term
* User median investment amount: 10000
```

### Output Format Example
```json
{{
  "investments": [
    {{
      "basket_name": "Healthcare Growth",
      "investment_amount": 5000.0
    }},
    {{
      "basket_name": "Low Volatility Dividend",
      "investment_amount": 3000.0
    }},
    {{
      "basket_name": "Technology Innovation",
      "investment_amount": 2000.0
    }}
  ]
}}
```

Here are all available stock baskets:
{all_basket_description}
  """
  
  USER_PROMPT = """
Please generate a list of investments for the user based on the following profile:
* User location: {user_location}
* User gender: {user_gender}
* User age: {user_age}
* User education: {user_education}
* User investment goal: {user_invest_goal}
* User median investment amount: {user_median_investment_amount}
  """

  def __init__(self, model_name: str, all_basket_description: str, max_number_of_investments: int, temperature: float = 0.8):
    self.client = OpenAI(
      api_key=os.getenv('OPENROUTER_API_KEY'),
      base_url='https://openrouter.ai/api/v1'
    )
    self.model_name = model_name
    self.temperature = temperature
    self.system_prompt = self.SYSTEM_PROMPT.format(
      all_basket_description=all_basket_description, 
      max_number_of_investments=max_number_of_investments
    )
    self.system_prompt = self.system_prompt.replace('{', '{{').replace('}', '}}')
    self.logger = logging.getLogger("LLMPurchaseGenerator")

  def generate_investment_by_user(self, user: User) -> Investments:
      user_prompt = self.USER_PROMPT.format(
          user_location=user.user_location,
          user_gender=user.user_gender,
          user_age=user.user_age,
          user_education=user.user_education,
          user_invest_goal=user.user_invest_goal,
          user_median_investment_amount=user.user_median_investment_amount
      )
      
      counter = 0
      while counter < 3:
        counter += 1
        try:
          response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=[
              {"role": "system", "content": self.system_prompt},
              {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
          )
          
          response_content = response.choices[0].message.content
          response_json = json.loads(response_content)
          return Investments(**response_json)
        except Exception as e:
          print(e, flush=True)
          time.sleep(5)
          continue