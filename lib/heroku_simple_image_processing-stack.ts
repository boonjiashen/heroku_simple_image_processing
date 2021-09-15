import * as sns from 'monocdk/aws-sns';
import * as subs from 'monocdk/aws-sns-subscriptions';
import * as sqs from 'monocdk/aws-sqs';
import * as cdk from 'monocdk';

export class HerokuSimpleImageProcessingStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const queue = new sqs.Queue(this, 'HerokuSimpleImageProcessingQueue', {
      visibilityTimeout: cdk.Duration.seconds(299)
    });

    const topic = new sns.Topic(this, 'HerokuSimpleImageProcessingTopic');

    topic.addSubscription(new subs.SqsSubscription(queue));
  }
}
