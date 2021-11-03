import boto3, logging, os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    apigw_client = boto3.client('apigateway')

    PROVIDER_ARN = os.environ['PROVIDER_ARN']
    
    logger.info(event["ResourceId"])
    ResourceId = event["ResourceId"]
    
    restApiId = event["ResourceId"].split("/")[2]
    logger.info(restApiId)
    
    restApiName = apigw_client.get_rest_api(
        restApiId=restApiId)['name']
    

    get_authorizers = apigw_client.get_authorizers(
        restApiId=restApiId)
    
    logger.info(get_authorizers)
    
    if get_authorizers["items"]: 
        logger.info("Authorizer found. No need to create one")
        authorizer_id = get_authorizers["items"][0]['id']
        
    else: 
        response = apigw_client.create_authorizer(
            restApiId=restApiId, 
            name=restApiName, 
            type='COGNITO_USER_POOLS',
            providerARNs=[
                PROVIDER_ARN
            ],
            identitySource='method.request.header.Auth'
        )
        authorizer_id = response['id']
    
    # now let us get all of the resources, and their IDs
    
    restApi_resources = apigw_client.get_resources(
        restApiId=restApiId
        )
    print("All api resources")
    logger.info(restApi_resources)

    
    for item in restApi_resources['items']: 
        print("Resource ID")
        logger.info(item['id'])
        api_resource_ID = item['id']
        
        
        # now let us update the method with the correct authorisation.
        # get a list of correct actions 
        list_of_actions = apigw_client.get_resource(
            restApiId=restApiId,
            resourceId=api_resource_ID
            )
        
        print("Full list of items ")
        logger.info(list_of_actions)
        print("An individual action")
        logger.info(list_of_actions['resourceMethods'])
        final_action_list = list(list_of_actions['resourceMethods'].keys())
        
        print('Printed neatly')
        logger.info(final_action_list)
        
        for action in final_action_list: 

            update_method_response = apigw_client.update_method(
                restApiId=restApiId,
                resourceId=api_resource_ID,
                httpMethod=action,
                patchOperations=[
                    {
                        'op': 'replace',
                        'path': "/authorizationType",
                        'value': "COGNITO_USER_POOLS",
                    },
                    {
                        'op': 'replace', 
                        'path': "/authorizerId",
                        'value': authorizer_id
                    },
                ]
            )
            
            logger.info(update_method_response)

    
