# LinkedIn article draft: Managing supplier performance needs more than a scorecard

**Author:** Shahid Al Parvez Malik  
**Status:** Draft; not published

In my IT operations work, supplier performance has rarely been a single number. Service context matters: the same SLA result can have a different operational impact depending on the service and contract.

I built a small local, runnable proof of concept to make that review process visible. It uses eight fictional contract records across planning, tender, evaluation, active service, and renewal review. The script checks the declared fields, calculates a transparent score from SLA performance, on-time delivery, and quality, and flags renewal dates that are close or already passed.

## A prompt for review, not a supplier verdict

On the sample data, the run flagged two renewal dates within 90 days, one date already passed, and four records for human review. Five records had performance metrics to score. These counts come from fictional input; they say nothing about real suppliers or service quality.

The score uses stated inputs and a documented formula. A missed SLA target stays visible even if other measures lift the combined score. Missing metrics in pipeline records are left unscored rather than guessed.

## Keep accountability with people

A scorecard cannot interpret a contract clause, confirm that the data is complete, weigh business continuity, or decide whether a supplier should be renewed. Procurement, service owners, finance, legal, and security each bring context the script does not have. The output should help a team prepare its review, not take the decision away from them.

This first version is rules-based, not an AI model. It uses synthetic data, has no connection to finance, ERP, ITSM, contract, or vendor systems, and executes no procurement actions. It is a software demonstration, not a production deployment or evidence of savings, supplier improvement, or accuracy in a live environment.

## The project

The repository contains the synthetic sample data, code, tests, scoring notes, and run instructions.

Repository link: https://github.com/shahidalparvezmalik/it-procurement-vendor-management

The aim is to explore how a manager might see lifecycle status, SLA performance, and renewal timing in one review pack, while keeping the inputs and limits clear. Before using real data, an organization would need approved sources, agreed definitions, validated thresholds, and its own approval and audit controls.

## About the author

Shahid Al Parvez Malik is a Senior IT Infrastructure & Service Delivery Manager with 20+ years of professional IT experience across enterprise infrastructure, IT Operations, ITSM, service delivery, systems administration, networking, technical support, IT procurement, and vendor management. He uses portfolio projects to explore practical, governed improvements to IT operations.

GitHub: https://github.com/shahidalparvezmalik  
Professional portfolio: https://shahidalparvezmalik.com/

#ITProcurement #VendorManagement #ITOperations #ITInfrastructure #ITSM #ServiceDelivery #SupplierManagement #IrishTech #IrishITTech #Ireland
