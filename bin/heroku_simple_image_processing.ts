#!/usr/bin/env node
import * as cdk from '@aws-cdk/core';
import { HerokuSimpleImageProcessingStack } from '../lib/heroku_simple_image_processing-stack';

const app = new cdk.App();
new HerokuSimpleImageProcessingStack(app, 'HerokuSimpleImageProcessingStack');
