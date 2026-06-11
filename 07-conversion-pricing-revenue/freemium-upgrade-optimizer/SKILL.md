---
name: freemium-upgrade-optimizer
description: Optimize SaaS paywall conversion by timing triggers, refining value propositions, and implementing high-converting pricing structures.
---

## When to Use
Use this skill when designing or auditing a SaaS product's upgrade flow. It applies to freemium models, free trials, and usage-based products looking to increase the percentage of free users who convert to paid plans.

## The Strategic Timing Principle
The most effective paywalls appear immediately after a user experiences the **"Aha Moment"** (the point where they realize the product's core value). 
- **Bad Timing**: Triggering a paywall during onboarding before the user has seen any results.
- **Good Timing**: Triggering a paywall when a user attempts to use a high-value "power feature" or hits a capacity limit after successful usage.

## Paywall Trigger Taxonomy
1. **Feature Gate**: User clicks a "Pro" feature (e.g., Advanced Analytics, Export to CSV).
2. **Usage Limit**: User reaches a hard cap (e.g., "You've used 5/5 free credits this month").
3. **Trial Expiry**: The time-limited access is ending (e.g., "Your 14-day trial expires in 48 hours").
4. **Contextual Nudge**: A soft prompt shown when a user repeatedly performs an action that would be easier/faster on a paid plan.

## Anatomy of a High-Converting Paywall
A standard paywall should include these 7 elements:
1. **Compelling Headline**: Focus on the benefit, not the price (e.g., "Unlock Unlimited Growth" vs "Choose a Plan").
2. **Value Preview**: Visual representation of what is being unlocked (blurred data, icon set, or short video).
3. **Feature Comparison**: A clear "Free vs. Pro" table. Limit the list to the top 5 most persuasive differences.
4. **Transparent Pricing**: Show monthly vs. annual toggles. Highlight the "Discounted Monthly" rate for annual plans.
5. **Social Proof**: One high-impact testimonial or "Trusted by 10,000+ teams."
6. **Frictionless CTA**: Clear, high-contrast button (e.g., "Start My 7-Day Free Trial").
7. **Exit Path**: A visible "Maybe Later" or "X" button to prevent user frustration, unless it is a hard lock.

## Conversion Psychology & Anti-Patterns
### Best Practices:
- **Default to Annual**: Pre-select the annual billing toggle (typically 20% discount).
- **The Decoy Effect**: Use a middle "Recommended" tier to make the target plan look like the best value.
- **Loss Aversion**: Use copy like "Don't lose your progress" or "Keep your 50% discount" for expiring trials.

### Anti-Patterns to Avoid:
- **Hidden Close Buttons**: Making it impossible to exit the paywall (destroys trust).
- **Plan Overload**: Offering more than 3-4 options (causes choice paralysis).
- **Guilt-Trip Copy**: Using buttons like "No, I prefer being unproductive" (creates negative brand sentiment).

## A/B Testing Framework
When optimizing, test one variable at a time:
- **Trigger Location**: Does the paywall convert better on the Dashboard or within the specific Workflow?
- **Trial Length**: 7 days (creates urgency) vs. 14 days (allows for deeper habit formation).
- **Pricing Display**: $120/year vs. $10/month billed annually.
- **Credit Card Requirement**: Testing "No CC required" for trials to increase sign-ups vs. "CC required" to increase lead quality.

## Fatigue & Frequency Management
- **Cooldown Periods**: If a user dismisses a soft paywall, do not show it again for at least 3-7 days.
- **Fatigue Signals**: If a user dismisses the paywall 3 times in one session, suppress all prompts for 24 hours to prevent churn.
- **Upgrade Path**: Ensure the "Upgrade" button is always accessible in the navigation, even when the paywall isn't triggered.
