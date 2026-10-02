def generate_career_advice(role, matched_skills, missing_skills):

    advice = []

    # --------------------------------------------------
    # Current skill status
    # --------------------------------------------------

    if matched_skills:
        advice.append(
            f"You already have {len(matched_skills)} "
            f"skills relevant to the {role} role."
        )
    else:
        advice.append(
            f"Your current skill list does not match "
            f"the analyzed requirements for the {role} role."
        )

    # --------------------------------------------------
    # Prioritize missing skills by job demand
    # --------------------------------------------------

    if missing_skills:

        priority_skills = sorted(
            missing_skills,
            key=lambda x: x["percentage"],
            reverse=True
        )

        top_missing = priority_skills[:5]

        skill_details = []

        for skill in top_missing:

            skill_details.append(
                f'{skill["skill"]} '
                f'({skill["percentage"]}% of analyzed postings)'
            )

        advice.append(
            "Prioritize learning these skills based on "
            "job-market demand: "
            + ", ".join(skill_details)
            + "."
        )

        # --------------------------------------------------
        # Highest priority skill
        # --------------------------------------------------

        top_skill = top_missing[0]

        advice.append(
            f"Start with {top_skill['skill']} because it "
            f"appears in {top_skill['percentage']}% of the "
            f"analyzed {role} job postings."
        )

    else:

        advice.append(
            f"Your current skills cover all tracked skills "
            f"for the {role} role in this dataset."
        )

    return advice