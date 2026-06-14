import { defineCollection, z } from 'astro:content';

const knowledge = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    topic: z.enum(['Advance Rent', 'Agreements', 'Rent Control', 'Eviction', 'Compliance']),
    pubDate: z.coerce.date(),
    lastReviewed: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { knowledge };
