# Expense Tracker Service

## Usage

All responses will have the form

```json
{
	"data": "Mixed type holding the content of the response",
	"message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

## List all expenses for the last 30 days

**Definition**

`GET /expenses`

**Response**

- `200 OK` on success

```json
[
	{
		"identifier": "{95bf6d07-df10-4427-afcc-e4b31727eec6}",
		"amount": 25.00,
		"category_name": "Food",
		"category_identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"merchant_name": "Moe's",
		"merchant_identifier": "{bbe2ac7f-ecd8-47f8-a883-ee109c00601e}",
		"transaction_utc": "2019-11-05T13:15:30Z"
	},
	{
		"identifier": "{7a448b4d-94a7-4ed9-ad07-58bb6607f02e}",
		"amount": 43.00,
		"category_name": "Entertainment",
		"category_identifier": "{4bbc33f0-a32e-4dd5-8636-86b790d67cfc}",
		"merchant_name": "NC Zoo",
		"merchant_identifier": "{b2086372-f068-4e85-9e6f-f684b68c1893}",
		"transaction_utc": "2019-11-05T13:15:30Z"
	}
]
```

## Lookup expense details

**Definition**

`GET /expenses/<identifier>` 

**Response**

- `404 Not Found` if the expense does not exist
- `200 OK` on success

```json
	{
		"identifier": "{95bf6d07-df10-4427-afcc-e4b31727eec6}",
		"amount": 25.00,
		"category_name": "Food",
		"category_identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"merchant_name": "Moe's",
		"merchant_identifier": "{bbe2ac7f-ecd8-47f8-a883-ee109c00601e}",
		"transaction_utc": "2019-11-05T13:15:30Z"
	}
```

## Record a new expense

**Defintion**

`POST /expenses`

**Arguments**

- `"identifier": uniqueidentifier` a globally unique identifier for this expense
- `"amount": decimal` the amount of the expense
- `"category_name": string` the name of the category
- `"category_identifier": uniqueidentifier` a globally unique identifier for the category of this expense
- `"merchant_name": string` the name of the merchant
- `"merchant_identifier": uniqueidentifier` a globally unique identifier for the merchant where this expense occurred
- `"transaction_utc": datetime` the datetime, in UTC format, of the transaction

**Response**

- `201 Created` on success

```json
	{
		"identifier": "{95bf6d07-df10-4427-afcc-e4b31727eec6}",
		"amount": 25.00,
		"category_name": "Food",
		"category_identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"merchant_name": "Moe's",
		"merchant_identifier": "{bbe2ac7f-ecd8-47f8-a883-ee109c00601e}",
		"transaction_utc": "2019-11-05T13:15:30Z"
	}
```

## Delete expense

- `DELETE /expenses/<identifier>`

**Response**

- `404 Not Found` if the expense does not exist
- `204 No Content` on success


## List all expense categories

**Definition**

`GET /categories`

**Response**

- `200 OK` on success

```json
[
	{
		"identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"name": "Food"
	},
	{
		"identifier": "{4bbc33f0-a32e-4dd5-8636-86b790d67cfc}",
		"name": "Entertainment"		
	}
]
```

## List category detail

**Definition**

- `GET /categories/<identifier>`

**Response**

- `404 Not Found` if the category does not exist
- `200 OK` on success

```json
	{
		"identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"name": "Food"
	}
```

## Add new category

**Definition**

- `POST /categories`

**Arguments**

- `"identifier": uniqueidentifier` a globally unique identifier for the category
- `"name": string` the name of the category

**Response**

- `201 Created` on success

```json
	{
		"identifier": "{e5536211-3690-437a-ab7b-9ef50e11f57b}",
		"name": "Food"
	}
```

## Delete a category

**Definition**

- `DELETE /categories/<identifier>`

**Response**

- `404 Not Found` if the category does not exist
- `204 No Content` on success
- `304 Not Modified` if there are expenses associated with this category

Note: if there are any expenses already associated with this category, the delete operation is not valid.

## List all merchants

**Definition**

`GET /merchants`

**Response**

- `200 OK` on success

```json
[
	{
		"identifier": "{b2086372-f068-4e85-9e6f-f684b68c1893}",
		"name": "NC Zoo"
	},
	{
		"identifier": "{bbe2ac7f-ecd8-47f8-a883-ee109c00601e}",
		"name": "Moe's"		
	}
]
```

## List merchant detail

**Definition**

- `GET /merchants/<identifier>`

**Response**

- `404 Not Found` if the merchant does not exist
- `200 OK` on success

```json
	{
		"identifier": "{b2086372-f068-4e85-9e6f-f684b68c1893}",
		"name": "NC Zoo"
	}
```

## Add new merchant

**Definition**

- `POST /merchants`

**Arguments**

- `"identifier": uniqueidentifier` a globally unique identifier for the merchant
- `"name": string` the name of the merchant

**Response**

- `201 Created` on success

```json
	{
		"identifier": "{b2086372-f068-4e85-9e6f-f684b68c1893}",
		"name": "NC Zoo"
	}
```

## Delete a category

**Definition**

- `DELETE /merchants/<identifier>`

**Response**

- `404 Not Found` if the merchant does not exist
- `204 No Content` on success
- `304 Not Modified` if there are expenses associated with this merchant

Note: if there are any expenses already associated with this merchant, the delete operation is not valid.