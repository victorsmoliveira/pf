<script>
	import { onMount } from "svelte";

	let metricsPerSectionData = [];
	let userMetricsData = {};
	let userResponseData = "";
	let formValid = true;
	let isSubmitted = false;
	let isError = false;
	// const UserId = "6aa8e943-d571-4226-a161-b7a7e387845c";
	const UserId = "504bfa75-34f6-4822-bc34-97d6547f260d";

	onMount(async () => {
		const userResponse = await fetch(
			"http://localhost:8000/users/" + UserId
		);
		userResponseData = await userResponse.json();

		// Fetch metrics per section
		const metricsPerSectionResponse = await fetch(
			"http://localhost:8000/metrics/metrics_per_section/"
		);
		metricsPerSectionData = await metricsPerSectionResponse.json();

		// Fetch user metrics
		const userMetricsResponse = await fetch(
			"http://localhost:8000/user_metrics/user/" + UserId
		);
		const userMetrics = await userMetricsResponse.json();
		userMetricsData = userMetrics["user_metrics"];
	});

	async function handleSubmit() {
		formValid = true;

		// Check if all fields are filled out
		for (let section of metricsPerSectionData) {
			for (let metric of section.metrics) {
				if (
					!userMetricsData[metric.id] &&
					userMetricsData[metric.id] !== 0
				) {
					formValid = false;
					break;
				}
			}
		}

		if (!formValid) {
			setTimeout(() => (formValid = true), 3000);
			return; // exit the function if the form isn't valid
		}

		let userMetrics = {};

		for (let section of metricsPerSectionData) {
			for (let metric of section.metrics) {
				let inputElement = document.getElementById(metric.id);
				if (!inputElement) continue; // If input element not found, skip to the next metric

				let value;

				switch (metric.data_type) {
					case "integer":
						value = parseInt(inputElement.value);
						break;
					case "decimal":
						value = parseFloat(inputElement.value);
						break;
					case "boolean":
						value = inputElement.checked; // Assuming this is a checkbox input
						break;
					case "string": // We don't need to do any conversions
					default:
						value = inputElement.value;
				}

				userMetrics[metric.id] = value;
			}
		}

		try {
			let response = await fetch(
				"http://localhost:8000/user_metrics/bulk",
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						user_id: UserId,
						user_metrics: userMetrics,
					}),
				}
			);

			if (!response.ok) {
				throw new Error("Network response was not ok");
			}

			let jsonResponse = await response.json();
			console.log(jsonResponse);

			isSubmitted = true;
			isError = false;
			setTimeout(() => (isSubmitted = false), 3000);
		} catch (error) {
			isError = true;
			console.log(
				"There was a problem with the fetch operation:",
				error.message
			);
		}
	}
</script>

<h1>Hello {userResponseData.username}!</h1>
<!-- Render the form -->
{#each metricsPerSectionData as section}
	<h2>{section.section_name}</h2>
	{#each section.metrics as metric}
		<div>
			<label for={metric.id}>{metric.metric_name}</label>
			{#if metric.data_type === "integer" || metric.data_type === "decimal"}
				<input
					type="number"
					id={metric.id}
					bind:value={userMetricsData[metric.id]}
					step={metric.data_type === "decimal" ? "0.1" : "1"}
				/>
			{:else if metric.data_type === "boolean"}
				<input
					type="checkbox"
					id={metric.id}
					bind:checked={userMetricsData[metric.id]}
				/>
			{:else if metric.data_type === "list"}
				<select id={metric.id} bind:value={userMetricsData[metric.id]}>
					{#each metric.data_properties.list_values as value}
						<option {value}>{value}</option>
					{/each}
				</select>
			{:else}
				<input
					type="text"
					id={metric.id}
					bind:value={userMetricsData[metric.id]}
				/>
			{/if}
		</div>
	{/each}
{/each}

<button on:click={handleSubmit}>Submit</button>

{#if !formValid}
	<div class="notification error">
		Please fill out all fields before submitting.
	</div>
{:else if isSubmitted}
	<div class="notification success">Form successfully submitted!</div>
{:else if isError}
	<div class="notification error">
		There was an error submitting the form. Please try again.
	</div>
{/if}
